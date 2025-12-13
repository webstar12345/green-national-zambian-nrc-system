# 🔐 OTP Email Verification System - Complete Guide

## 📋 Overview

Your NRC system now has a complete OTP (One-Time Password) email verification system that enhances security for both registration and login processes.

## 🔄 How It Works

### 📝 **Registration Flow**
1. **User fills signup form** → Account created
2. **OTP generated** → 6-digit code created
3. **Email sent** → HTML formatted email with OTP
4. **User verifies** → Enters OTP code
5. **Account activated** → User logged in and verified

### 🔑 **Login Flow**
1. **User enters credentials** → Username/password verified
2. **OTP generated** → 6-digit code created
3. **Email sent** → HTML formatted email with OTP
4. **User verifies** → Enters OTP code
5. **Login completed** → User logged in successfully

## 📧 Email Features

### ✅ **Professional Design**
- NRC Zambia branding
- Zambian green color scheme
- Clean, responsive layout
- Official government styling

### ✅ **Security Features**
- 10-minute expiration
- Security warnings
- Anti-phishing tips
- Clear instructions

### ✅ **Technical Features**
- HTML + Plain text versions
- Mobile-friendly design
- Proper email headers
- Error handling

## 🛠️ Technical Implementation

### **Models Enhanced**
- `CustomUser.generate_otp()` - Creates 6-digit code
- `CustomUser.verify_otp()` - Validates and expires code
- OTP fields: `otp_code`, `otp_created_at`, `otp_verified`

### **Views Updated**
- `CustomLoginView` - Integrated OTP verification
- `SignUpView` - Added OTP step after registration
- `otp_verify` - Handles both login and signup OTP
- `resend_otp` - Resends expired codes

### **Templates Created**
- `otp_verify.html` - OTP input form
- `otp_email.html` - HTML email template
- Enhanced with context-aware messaging

### **Services Added**
- `OTPService` - Email sending and validation
- HTML email rendering
- Error handling and logging

## 🔧 Configuration

### **Email Settings** (in settings.py)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@zambiannrc.gov.zm'
```

### **Environment Variables** (in .env)
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@zambiannrc.gov.zm
```

## 🎯 User Experience

### **For New Users (Registration)**
1. Fill signup form with email
2. See message: "Account created! Check your email for verification code"
3. Receive professional email with 6-digit code
4. Enter code on verification page
5. Account verified and logged in automatically

### **For Existing Users (Login)**
1. Enter username and password
2. See message: "OTP sent to your email"
3. Receive email with 6-digit code
4. Enter code on verification page
5. Logged in successfully

### **Security Features**
- Codes expire in 10 minutes
- Can request new code if expired
- Clear error messages for invalid codes
- Session management prevents bypassing

## 🧪 Testing

### **Test OTP System**
```bash
python test_otp_email.py
```

### **Manual Testing**
1. **Registration Test:**
   - Go to signup page
   - Fill form with valid email
   - Check email for OTP
   - Enter OTP code
   - Verify login success

2. **Login Test:**
   - Go to login page
   - Enter valid credentials
   - Check email for OTP
   - Enter OTP code
   - Verify login success

3. **Error Testing:**
   - Try invalid OTP codes
   - Test expired codes
   - Test resend functionality

## 🚀 Deployment

### **Deploy Command**
```bash
git add .
git commit -m "Deploy OTP email verification system"
git push origin main
```

### **Verify Deployment**
1. Visit live site
2. Test registration flow
3. Test login flow
4. Check email delivery
5. Verify all error cases

## 🔍 Troubleshooting

### **Common Issues**

**1. Emails Not Sending**
- Check email configuration in settings
- Verify SMTP credentials
- Check spam/junk folders
- Test with different email providers

**2. OTP Codes Not Working**
- Check code expiration (10 minutes)
- Verify exact code entry (no spaces)
- Test resend functionality
- Check session management

**3. Template Errors**
- Verify template files exist
- Check template syntax
- Test HTML rendering
- Fallback to plain text

### **Debug Commands**
```bash
# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])

# Test OTP generation
>>> from accounts.models import CustomUser
>>> user = CustomUser.objects.first()
>>> otp = user.generate_otp()
>>> print(otp)
```

## 📊 Security Benefits

### ✅ **Enhanced Security**
- Two-factor authentication
- Email verification required
- Time-limited codes
- Session-based verification

### ✅ **User Trust**
- Professional email design
- Clear security messaging
- Government branding
- Transparent process

### ✅ **Compliance**
- Secure authentication
- Audit trail capability
- User verification
- Data protection

## 🎉 Success Metrics

- ✅ **Registration security** - Email verification required
- ✅ **Login security** - OTP verification for all logins
- ✅ **Professional emails** - HTML formatted with branding
- ✅ **User experience** - Clear instructions and feedback
- ✅ **Error handling** - Graceful failure and recovery
- ✅ **Mobile friendly** - Responsive design for all devices

Your OTP email verification system is now complete and ready for production use!