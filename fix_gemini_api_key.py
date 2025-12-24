#!/usr/bin/env python
"""
Fix Gemini API Key - Replace Leaked Key
The current Gemini API key was reported as leaked and needs to be replaced.
"""

import os
from decouple import config

def fix_gemini_api_key():
    """Fix the leaked Gemini API key"""
    print("🔐 GEMINI API KEY SECURITY FIX")
    print("=" * 50)
    print()
    
    current_key = config('GEMINI_API_KEY', default='')
    if current_key:
        print(f"❌ Current key (LEAKED): {current_key[:10]}...{current_key[-4:]}")
    else:
        print("❌ No Gemini API key found in .env")
    
    print()
    print("🚨 SECURITY ALERT:")
    print("Your Gemini API key was reported as leaked and has been disabled.")
    print("You need to generate a new API key to restore AI functionality.")
    print()
    
    print("📋 STEPS TO FIX:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the new API key")
    print("5. Update your .env file:")
    print("   GEMINI_API_KEY=your_new_api_key_here")
    print()
    
    print("🔧 TEMPORARY WORKAROUND:")
    print("The system will continue to work without AI features.")
    print("Chat widget and AI assistant will show error messages until fixed.")
    print()
    
    # Disable the current leaked key
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Comment out the leaked key
        if 'GEMINI_API_KEY=AIzaSyAOmQ21LSQMA9u0OB_3fBFeeU3moS6jyNk' in content:
            content = content.replace(
                'GEMINI_API_KEY=AIzaSyAOmQ21LSQMA9u0OB_3fBFeeU3moS6jyNk',
                '# GEMINI_API_KEY=LEAKED_KEY_DISABLED\n# Get new key from: https://makersuite.google.com/app/apikey\nGEMINI_API_KEY='
            )
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✅ Leaked API key disabled in .env file")
            print("💡 Add your new API key after GEMINI_API_KEY=")
        else:
            print("ℹ️  API key already updated or not found")
    
    print()
    print("🔒 SECURITY BEST PRACTICES:")
    print("- Never commit API keys to Git repositories")
    print("- Use environment variables for sensitive data")
    print("- Regularly rotate API keys")
    print("- Monitor for leaked credentials")

if __name__ == "__main__":
    fix_gemini_api_key()