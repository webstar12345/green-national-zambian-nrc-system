#!/usr/bin/env python3
"""
Production Environment Update Helper
Updates Render.com environment variables securely
"""

def print_render_instructions():
    """Instructions for updating Render.com environment variables"""
    print("🚀 Updating Production Environment (Render.com)")
    print("=" * 50)
    print()
    print("📋 STEP-BY-STEP INSTRUCTIONS:")
    print()
    print("1. 🌐 Go to Render.com Dashboard:")
    print("   https://dashboard.render.com/")
    print()
    print("2. 🔍 Find your NRC System service:")
    print("   - Look for 'green-national-zambian-nrc-system'")
    print("   - Click on the service name")
    print()
    print("3. ⚙️  Go to Environment tab:")
    print("   - Click 'Environment' in the left sidebar")
    print("   - You'll see a list of environment variables")
    print()
    print("4. 🔄 Update/Add these variables:")
    print()
    
    email = input("Enter your Gmail address (simoongalaurent427@gmail.com): ").strip()
    if not email:
        email = "simoongalaurent427@gmail.com"
    
    new_password = input("Enter your NEW 16-character app password: ").strip()
    
    if len(new_password) != 16:
        print("❌ Invalid password length! Should be 16 characters.")
        return
    
    print("   📧 EMAIL VARIABLES TO SET:")
    print(f"   EMAIL_HOST_USER = {email}")
    print(f"   EMAIL_HOST_PASSWORD = {new_password}")
    print("   EMAIL_HOST = smtp.gmail.com")
    print("   EMAIL_PORT = 587")
    print("   EMAIL_USE_TLS = True")
    print(f"   DEFAULT_FROM_EMAIL = {email}")
    print()
    print("5. 💾 Save changes:")
    print("   - Click 'Save Changes' button")
    print("   - Render will automatically redeploy your service")
    print()
    print("6. ⏳ Wait for deployment:")
    print("   - Watch the deployment logs")
    print("   - Wait for 'Deploy successful' message")
    print()
    print("7. 🧪 Test OTP emails:")
    print("   - Go to your live site")
    print("   - Try to login/register")
    print("   - Check if OTP emails arrive")
    print()

def print_environment_variables():
    """Print environment variables in different formats"""
    print("📋 Environment Variables Reference")
    print("=" * 40)
    
    email = input("Gmail address: ").strip()
    password = input("New app password: ").strip()
    
    print("\n🔧 For Render.com Environment Tab:")
    print("-" * 40)
    print(f"EMAIL_HOST_USER={email}")
    print(f"EMAIL_HOST_PASSWORD={password}")
    print("EMAIL_HOST=smtp.gmail.com")
    print("EMAIL_PORT=587")
    print("EMAIL_USE_TLS=True")
    print(f"DEFAULT_FROM_EMAIL={email}")
    print()
    
    print("📝 For .env file:")
    print("-" * 40)
    print(f"EMAIL_HOST_USER={email}")
    print(f"EMAIL_HOST_PASSWORD={password}")
    print("EMAIL_HOST=smtp.gmail.com")
    print("EMAIL_PORT=587")
    print("EMAIL_USE_TLS=True")
    print(f"DEFAULT_FROM_EMAIL={email}")
    print()

def check_deployment_status():
    """Instructions for checking deployment status"""
    print("🔍 Checking Deployment Status")
    print("=" * 35)
    print()
    print("1. 📊 In Render.com Dashboard:")
    print("   - Go to your service page")
    print("   - Check 'Events' tab for deployment status")
    print("   - Look for 'Deploy successful' message")
    print()
    print("2. 📋 Check Logs:")
    print("   - Click 'Logs' tab")
    print("   - Look for any email-related errors")
    print("   - Check for Django startup messages")
    print()
    print("3. 🧪 Test Live Site:")
    print("   - Go to your live URL")
    print("   - Try login/registration")
    print("   - Check if OTP emails arrive")
    print()
    print("4. 🔧 If still not working:")
    print("   - Check environment variables are set correctly")
    print("   - Verify new Gmail app password is active")
    print("   - Check Django logs for SMTP errors")
    print()

def main():
    """Main function"""
    print("🚀 PRODUCTION ENVIRONMENT UPDATE TOOL")
    print("=" * 45)
    print()
    print("⚠️  SECURITY BREACH RESPONSE:")
    print("   Old Gmail credentials were exposed in GitHub")
    print("   Production environment needs new credentials")
    print()
    
    while True:
        print("Choose an option:")
        print("1. 📖 Render.com update instructions")
        print("2. 📋 Generate environment variables")
        print("3. 🔍 Check deployment status")
        print("4. 🚪 Exit")
        print()
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == '1':
            print_render_instructions()
        elif choice == '2':
            print_environment_variables()
        elif choice == '3':
            check_deployment_status()
        elif choice == '4':
            print("✅ Remember to test OTP emails after updating!")
            break
        else:
            print("❌ Invalid choice!")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()