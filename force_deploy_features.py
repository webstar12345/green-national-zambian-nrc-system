#!/usr/bin/env python
"""
Force deploy all features by ensuring they're properly committed
"""
import os
import subprocess

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def check_git_status():
    """Check what files are staged/unstaged"""
    print("🔍 Checking Git Status...")
    stdout, stderr, code = run_command("git status --porcelain")
    
    if stdout.strip():
        print("📝 Files that need to be committed:")
        for line in stdout.strip().split('\n'):
            print(f"  {line}")
        return True
    else:
        print("✅ All files are committed")
        return False

def force_add_all_files():
    """Force add all files including new ones"""
    print("\n📦 Force adding all files...")
    
    # Add all files
    stdout, stderr, code = run_command("git add .")
    if code == 0:
        print("✅ All files added")
    else:
        print(f"❌ Error adding files: {stderr}")
    
    # Check status again
    stdout, stderr, code = run_command("git status --porcelain")
    if stdout.strip():
        print("📝 Files to be committed:")
        for line in stdout.strip().split('\n'):
            print(f"  {line}")
        return True
    return False

def commit_and_push():
    """Commit and push changes"""
    print("\n🚀 Committing and pushing changes...")
    
    # Commit
    commit_msg = "Force deploy all features: OTP, Dark Mode, AI Assistant, PWA, Animations, OAuth, Landing Page"
    stdout, stderr, code = run_command(f'git commit -m "{commit_msg}"')
    
    if code == 0:
        print("✅ Changes committed")
        
        # Push
        stdout, stderr, code = run_command("git push origin main")
        if code == 0:
            print("✅ Changes pushed to main branch")
            print("\n🎉 Deployment triggered! Check Render dashboard.")
            return True
        else:
            print(f"❌ Error pushing: {stderr}")
    else:
        if "nothing to commit" in stderr:
            print("ℹ️  No changes to commit - all files already up to date")
            return True
        else:
            print(f"❌ Error committing: {stderr}")
    
    return False

def main():
    """Main function"""
    print("🚀 FORCE DEPLOY ALL FEATURES")
    print("=" * 40)
    
    # Check current status
    has_changes = check_git_status()
    
    # Force add all files
    has_changes = force_add_all_files() or has_changes
    
    if has_changes:
        # Commit and push
        success = commit_and_push()
        if success:
            print("\n✅ SUCCESS! Features should appear on live site in 2-5 minutes")
            print("🌐 URL: https://green-national-zambian-nrc-system.onrender.com")
            print("\n🔄 If features still don't show:")
            print("1. Hard refresh browser (Ctrl+F5)")
            print("2. Clear browser cache")
            print("3. Try incognito mode")
            print("4. Wait 5 more minutes")
        else:
            print("\n❌ Deployment failed. Check errors above.")
    else:
        print("\n✅ All files are already committed and pushed")
        print("🔄 If features aren't showing, try:")
        print("1. Hard refresh browser (Ctrl+F5)")
        print("2. Clear browser cache")
        print("3. Check Render logs for errors")

if __name__ == '__main__':
    main()