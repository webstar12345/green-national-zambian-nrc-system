#!/usr/bin/env python
"""
Check which features are properly configured for deployment
"""
import os

def check_feature_files():
    """Check if all feature files are present"""
    print("🔍 Checking Feature Files for Deployment")
    print("=" * 50)
    
    features = {
        "OTP System": [
            "accounts/models.py",
            "accounts/views.py", 
            "templates/accounts/otp_verify.html",
            "accounts/otp_service.py"
        ],
        "Dark Mode": [
            "static/css/dark-mode.css",
            "static/js/dark-mode.js"
        ],
        "AI Assistant": [
            "applications/ai_assistant.py",
            "static/js/chat-widget.js",
            "static/css/chat-widget.css",
            "templates/applications/ai_demo.html"
        ],
        "PWA Features": [
            "static/manifest.json",
            "static/sw.js",
            "static/js/pwa-install.js"
        ],
        "Animations": [
            "static/css/animations.css",
            "static/js/animations.js"
        ],
        "Google OAuth": [
            "accounts/adapters.py",
            "templates/accounts/google_otp_verify.html"
        ]
    }
    
    all_present = True
    
    for feature_name, files in features.items():
        print(f"\n📋 {feature_name}:")
        feature_complete = True
        
        for file_path in files:
            if os.path.exists(file_path):
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path} - MISSING")
                feature_complete = False
                all_present = False
        
        if feature_complete:
            print(f"  🎯 {feature_name}: READY FOR DEPLOYMENT")
        else:
            print(f"  ⚠️  {feature_name}: INCOMPLETE")
    
    print(f"\n{'='*50}")
    if all_present:
        print("✅ ALL FEATURES READY FOR DEPLOYMENT!")
        print("\n🚀 Next steps:")
        print("1. Run: git add .")
        print("2. Run: git commit -m 'Deploy all features'")
        print("3. Run: git push origin main")
        print("4. Wait for Render to rebuild")
    else:
        print("⚠️  Some features are missing files")
        print("Check the missing files above")

if __name__ == '__main__':
    check_feature_files()