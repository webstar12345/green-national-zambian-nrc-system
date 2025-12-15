#!/usr/bin/env python3
"""
Production OTP Troubleshooting Tool
Helps diagnose why OTP emails aren't working in production
"""

def check_production_status():
    """Check production deployment and environment status"""
    print("🔍 Production OTP Troubleshooting")
    print("=" * 45)
    print()
    
    print("📋 CHECKLIST - Mark what you've completed:")
    print()
    
    # Local verification
    print("🏠 LOCAL ENVIRONMENT:")
    local_updated = input("✅ Updated local .env file with new password? (y/n): ").lower() == 'y'
    local_tested = input("✅ Tested local OTP emails successfully? (y/n): ").lower() == 'y'
    
    print()
    
    # GitHub push
    print("📦 GITHUB REPOSITORY:")
    github_pushed = input("✅ Pushed security fixes to GitHub? (y/n): ").lower() == 'y'
    
    print()
    
    # Production environment
    print("🚀 RENDER.COM PRODUCTION:")
    render_updated = input("✅ Updated Render.com environment variables? (y/n): ").lower() == 'y'
    render_deployed = input("✅ Waited for automatic redeployment? (y/n): ").lower() == 'y'
    
    print()
    
    # Production testing
    print("🧪 PRODUCTION TESTING:")
    prod_tested = input("✅ Tested OTP on live site? (y/n): ").lower() == 'y'
    
    print()
    print("🔍 DIAGNOSIS:")
    print("=" * 20)
    
    if not local_updated or not local_tested:
        print("❌ LOCAL ISSUE: Fix local environment first")
        return "local"
    
    if not github_pushed:
        print("❌ GITHUB ISSUE: Need to push changes to GitHub")
        return "github"
    
    if not render_updated:
        print("❌ RENDER ISSUE: Need to update Render.com environment variables")
        return "render"
    
    if not render_deployed:
        print("⏳ DEPLOYMENT ISSUE: Need to wait for Render.com redeployment")
        return "deployment"
    
    if not prod_tested:
        print("🧪 TESTING NEEDED: Try OTP on live site")
        return "testing"
    
    print("🔧 ALL STEPS COMPLETED - Need deeper diagnosis")
    return "advanced"

def provide_solution(issue_type):
    """Provide specific solution based on issue type"""
    print()
    print("🛠️ SOLUTION:")
    print("=" * 15)
    
    if issue_type == "local":
        print("1. Run: python test_new_password.py")
        print("2. Run: python test_otp_local.py")
        print("3. Verify both tests pass before proceeding")
    
    elif issue_type == "github":
        print("🚀 PUSH TO GITHUB:")
        print("Open Git Bash and run:")
        print("git add .")
        print('git commit -m "Security fix: Updated Gmail app password"')
        print("git push origin main")
    
    elif issue_type == "render":
        print("🌐 UPDATE RENDER.COM:")
        print("1. Go to: https://dashboard.render.com/")
        print("2. Find: green-national-zambian-nrc-system")
        print("3. Click: Environment tab")
        print("4. Update: EMAIL_HOST_PASSWORD=uroaoegylbpusjfy")
        print("5. Click: Save Changes")
    
    elif issue_type == "deployment":
        print("⏳ WAIT FOR DEPLOYMENT:")
        print("1. Check Render.com dashboard")
        print("2. Look for 'Deploy successful' message")
        print("3. Usually takes 2-3 minutes")
        print("4. Check logs for any errors")
    
    elif issue_type == "testing":
        print("🧪 TEST PRODUCTION:")
        print("1. Go to your live site")
        print("2. Try to login/register")
        print("3. Check email (including spam folder)")
        print("4. Wait up to 2 minutes for email delivery")
    
    elif issue_type == "advanced":
        print("🔧 ADVANCED TROUBLESHOOTING:")
        print("1. Check Render.com logs for SMTP errors")
        print("2. Verify environment variables are set correctly")
        print("3. Check if Gmail app password is still active")
        print("4. Try generating another new app password")

def check_render_environment():
    """Help check Render.com environment variables"""
    print()
    print("🔍 RENDER.COM ENVIRONMENT CHECK")
    print("=" * 35)
    print()
    print("📋 Required Environment Variables:")
    print("EMAIL_HOST_USER=simoongalaurent427@gmail.com")
    print("EMAIL_HOST_PASSWORD=uroaoegylbpusjfy")
    print("EMAIL_HOST=smtp.gmail.com")
    print("EMAIL_PORT=587")
    print("EMAIL_USE_TLS=True")
    print("DEFAULT_FROM_EMAIL=simoongalaurent427@gmail.com")
    print()
    print("🔍 How to verify:")
    print("1. Go to Render.com dashboard")
    print("2. Click on your service")
    print("3. Go to Environment tab")
    print("4. Check all variables are set correctly")
    print("5. Look for any typos or missing values")

def main():
    """Main troubleshooting function"""
    print("🚨 PRODUCTION OTP TROUBLESHOOTING")
    print("=" * 40)
    print()
    print("This tool will help diagnose why OTP emails")
    print("aren't working in production.")
    print()
    
    while True:
        print("Choose an option:")
        print("1. 🔍 Run diagnosis checklist")
        print("2. 🌐 Check Render.com environment")
        print("3. 🧪 Test local OTP (verify working)")
        print("4. 📋 Show production update steps")
        print("5. 🚪 Exit")
        print()
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            issue_type = check_production_status()
            provide_solution(issue_type)
        elif choice == '2':
            check_render_environment()
        elif choice == '3':
            print("🧪 Testing local OTP...")
            import subprocess
            try:
                result = subprocess.run(['python', 'test_otp_local.py'], 
                                      capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print("Errors:", result.stderr)
            except Exception as e:
                print(f"Error running test: {e}")
        elif choice == '4':
            print("📋 PRODUCTION UPDATE STEPS:")
            print("1. Push to GitHub: git add . && git commit -m 'Security fix' && git push origin main")
            print("2. Update Render.com: Environment → EMAIL_HOST_PASSWORD=uroaoegylbpusjfy")
            print("3. Wait for deployment: Check dashboard for 'Deploy successful'")
            print("4. Test live site: Try login/register and check email")
        elif choice == '5':
            break
        else:
            print("❌ Invalid choice!")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()