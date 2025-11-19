from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, UserProfileForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('applications:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
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


# Google OAuth with OTP Verification
from django.core.mail import send_mail
from django.conf import settings
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

@receiver(pre_social_login)
def handle_google_login(sender, request, sociallogin, **kwargs):
    """
    Handle Google OAuth login - generate and send OTP
    """
    # Get or create user
    user = sociallogin.user
    
    # If user is new or not verified, generate OTP
    if not user.pk or not user.otp_verified:
        # Generate OTP
        otp_code = user.generate_otp() if user.pk else None
        
        # Store user email in session for OTP verification
        request.session['pending_google_email'] = user.email
        request.session['pending_google_user_id'] = user.pk if user.pk else None
        
        # Send OTP email
        if user.email:
            send_otp_email(user.email, otp_code if otp_code else '000000')
        
        # Prevent automatic login
        sociallogin.state['process'] = 'connect'
        
        # Redirect to OTP verification page
        request.session['otp_required'] = True


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


def resend_otp(request):
    """Resend OTP code"""
    email = request.session.get('pending_google_email')
    user_id = request.session.get('pending_google_user_id')
    
    if not email:
        messages.error(request, 'Session expired. Please try logging in again.')
        return redirect('accounts:login')
    
    from .models import CustomUser
    try:
        if user_id:
            user = CustomUser.objects.get(pk=user_id)
        else:
            user = CustomUser.objects.get(email=email)
        
        # Generate new OTP
        otp_code = user.generate_otp()
        
        # Send email
        send_otp_email(user.email, otp_code)
        
        messages.success(request, 'New OTP code sent to your email!')
    
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
    
    return redirect('accounts:google_otp_verify')
