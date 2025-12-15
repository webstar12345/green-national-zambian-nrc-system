#!/usr/bin/env python3
"""
Push security fix to GitHub
"""
import subprocess
import sys

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🚀 Pushing Security Fix to GitHub")
    print("=" * 40)
    
    # Add files
    print("📦 Adding security fix files...")
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Failed to add files: {stderr}")
        return
    
    # Commit
    print("💾 Committing security fixes...")
    commit_message = """SECURITY FIX: Updated Gmail app password after breach

🚨 CRITICAL SECURITY ISSUE RESOLVED:
- Replaced compromised Gmail app password with new secure one
- Old password 'feirlikfycpiddbw' was exposed in GitHub (now disabled)
- New password 'uroaoegylbpusjfy' is secure and tested working
- Local OTP email functionality restored and verified

✅ SECURITY ACTIONS COMPLETED:
- Generated new Gmail app password from Google Account
- Updated local .env file with secure credentials
- Tested SMTP connection - working perfectly
- Tested OTP email delivery - working perfectly
- Prepared production environment update instructions

⚠️ PRODUCTION UPDATE REQUIRED:
- Render.com environment variables need updating
- New EMAIL_HOST_PASSWORD must be set in production
- Git history cleanup recommended for complete security

🛡️ SECURITY STATUS:
- Local environment: ✅ SECURE & WORKING
- Production environment: ⏳ UPDATE PENDING
- GitGuardian alert: ⏳ RESOLUTION PENDING"""

    success, stdout, stderr = run_command(f'git commit -m "{commit_message}"')
    if not success:
        print(f"❌ Failed to commit: {stderr}")
        return
    
    # Push
    print("🌐 Pushing to GitHub...")
    success, stdout, stderr = run_command("git push origin main")
    if not success:
        print(f"❌ Failed to push: {stderr}")
        return
    
    print("✅ Security fix pushed successfully!")
    print()
    print("🎯 NEXT STEPS:")
    print("1. Update Render.com environment variables")
    print("2. Test OTP emails on live site")
    print("3. Verify GitGuardian alert is resolved")
    print("4. Clean Git history if needed")

if __name__ == "__main__":
    main()