from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, UserProfileForm
from .otp_service import OTPService

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """Override to add OTP verification step"""
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate and send OTP
            otp_code = user.generate_otp()
            success = OTPService.send_otp_email(
                user.email, 
                otp_code, 
                user.get_full_name() or user.username
            )
            
            if success:
                # Store user info in session for OTP verification
                self.request.session['pending_login_user_id'] = user.id
                self.request.session['pending_login_email'] = user.email
                
                messages.success(
                    self.request, 
                    f'OTP verification code sent to {user.email}. Please check your email.'
                )
                return redirect('accounts:otp_verify')
            else:
                messages.error(self.request, 'Failed to send OTP email. Please try again.')
                return self.form_invalid(form)
        
        return super().form_valid(form)

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:otp_verify')

    def form_valid(self, form):
        """Override to add OTP verification step after signup"""
        # Save user but don't log them in yet
        response = super().form_valid(form)
        user = self.object
        
        # Generate and send OTP for email verification
        otp_code = user.generate_otp()
        success = OTPService.send_otp_email(
            user.email, 
            otp_code, 
            user.get_full_name() or user.username
        )
        
        if success:
            # Store user info in session for OTP verification
            self.request.session['pending_signup_user_id'] = user.id
            self.request.session['pending_signup_email'] = user.email
            
            messages.success(
                self.request, 
                f'Account created! OTP verification code sent to {user.email}. Please verify to complete registration.'
            )
        else:
            messages.error(self.request, 'Account created but failed to send verification email. Please contact support.')
        
        return response


@login_required
def profile(request):
    """User profile view with activity history"""
    from applications.models import NRCApplication
    
    # Get user's applications
    applications = NRCApplication.objects.filter(user=request.user).order_by('-created_at')
    
    # Get statistics
    total_applications = applications.count()
    approved_applications = applications.filter(status='approved').count()
    pending_applications = applications.filter(status='pending').count()
    
    context = {
        'applications': applications[:5],  # Recent 5
        'total_applications': total_applications,
        'approved_applications': approved_applications,
        'pending_applications': pending_applications,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


# Password Reset Views
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


# Google OAuth with OTP Verification (DISABLED FOR TESTING)
from django.core.mail import send_mail
from django.conf import settings
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

# TEMPORARILY DISABLED - This was causing the redirect loop
# @receiver(pre_social_login)
def handle_google_login_disabled(sender, request, sociallogin, **kwargs):
    """
    Handle Google OAuth login - generate and send OTP
    DISABLED: This was preventing Google OAuth from working
    """
    pass


def send_otp_email(email, otp_code):
    """Send OTP code via email"""
    subject = 'NRC Zambia - Login Verification Code'
    message = f"""
    Hello,
    
    Your verification code for NRC Zambia login is: {otp_code}
    
    This code will expire in 10 minutes.
    
    If you didn't request this code, please ignore this email.
    
    Best regards,
    NRC Zambia Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send OTP email: {e}")


def google_otp_verify(request):
    """Verify OTP for Google OAuth login"""
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '').strip()
        email = request.session.get('pending_google_email')
        user_id = request.session.get('pending_google_user_id')
        
        if not email:
            messages.error(request, 'Session expired. Please try logging in again.')
            return redirect('accounts:login')
        
        # Get user
        from .models import CustomUser
        try:
            if user_id:
                user = CustomUser.objects.get(pk=user_id)
            else:
                user = CustomUser.objects.get(email=email)
            
            # Verify OTP
            if user.verify_otp(otp_code):
                # OTP verified, log user in
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                # Clear session
                request.session.pop('pending_google_email', None)
                request.session.pop('pending_google_user_id', None)
                request.session.pop('otp_required', None)
                
                messages.success(request, 'Successfully logged in with Google!')
                return redirect('applications:home')
            else:
                messages.error(request, 'Invalid or expired OTP code. Please try again.')
        
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found. Please try logging in again.')
            return redirect('accounts:login')
    
    # GET request - show OTP form
    email = request.session.get('pending_google_email')
    if not email:
        return redirect('accounts:login')
    
    return render(request, 'accounts/google_otp_verify.html', {'email': email})


def otp_verify(request):
    """Enhanced OTP verification for both login and signup"""
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '').strip()
        
        # Check for pending login verification
        pending_login_user_id = request.session.get('pending_login_user_id')
        pending_signup_user_id = request.session.get('pending_signup_user_id')
        
        user = None
        verification_type = None
        
        if pending_login_user_id:
            try:
                user = User.objects.get(id=pending_login_user_id)
                verification_type = 'login'
            except User.DoesNotExist:
                messages.error(request, 'Invalid session. Please try logging in again.')
                return redirect('accounts:login')
                
        elif pending_signup_user_id:
            try:
                user = User.objects.get(id=pending_signup_user_id)
                verification_type = 'signup'
            except User.DoesNotExist:
                messages.error(request, 'Invalid session. Please try signing up again.')
                return redirect('accounts:signup')
        else:
            messages.error(request, 'No pending verification. Please log in or sign up first.')
            return redirect('accounts:login')
        
        # Verify OTP
        if user and user.verify_otp(otp_code):
            if verification_type == 'login':
                # Complete login process
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                # Clear session data
                request.session.pop('pending_login_user_id', None)
                request.session.pop('pending_login_email', None)
                
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('applications:home')
                
            elif verification_type == 'signup':
                # Complete signup process
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                # Clear session data
                request.session.pop('pending_signup_user_id', None)
                request.session.pop('pending_signup_email', None)
                
                messages.success(request, f'Welcome to NRC Zambia, {user.get_full_name() or user.username}! Your account has been verified.')
                return redirect('applications:home')
        else:
            messages.error(request, 'Invalid or expired OTP code. Please try again.')
    
    # Determine context for template
    context = {
        'verification_type': 'login' if request.session.get('pending_login_user_id') else 'signup',
        'email': request.session.get('pending_login_email') or request.session.get('pending_signup_email')
    }
    
    return render(request, 'accounts/otp_verify.html', context)

def resend_otp(request):
    """Resend OTP code for login or signup verification"""
    # Check for pending verification
    pending_login_user_id = request.session.get('pending_login_user_id')
    pending_signup_user_id = request.session.get('pending_signup_user_id')
    pending_google_email = request.session.get('pending_google_email')
    
    user = None
    redirect_url = 'accounts:otp_verify'
    
    if pending_login_user_id:
        try:
            user = User.objects.get(id=pending_login_user_id)
        except User.DoesNotExist:
            messages.error(request, 'Invalid session. Please try logging in again.')
            return redirect('accounts:login')
    elif pending_signup_user_id:
        try:
            user = User.objects.get(id=pending_signup_user_id)
        except User.DoesNotExist:
            messages.error(request, 'Invalid session. Please try signing up again.')
            return redirect('accounts:signup')
    elif pending_google_email:
        # Handle Google OAuth OTP resend
        user_id = request.session.get('pending_google_user_id')
        try:
            if user_id:
                user = User.objects.get(pk=user_id)
            else:
                user = User.objects.get(email=pending_google_email)
            redirect_url = 'accounts:google_otp_verify'
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('accounts:login')
    else:
        messages.error(request, 'No pending verification. Please log in or sign up first.')
        return redirect('accounts:login')
    
    if user:
        # Generate new OTP
        otp_code = user.generate_otp()
        
        # Send email
        success = OTPService.send_otp_email(
            user.email, 
            otp_code, 
            user.get_full_name() or user.username
        )
        
        if success:
            messages.success(request, f'New OTP code sent to {user.email}!')
        else:
            messages.error(request, 'Failed to send OTP email. Please try again.')
    
    return redirect(redirect_url)
