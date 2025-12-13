"""
Configuration checker for AI Assistant setup
Run this to verify your environment is properly configured
"""
import os
import sys

def check_setup():
    print("=" * 60)
    print("AI Assistant Setup Checker")
    print("=" * 60)
    print()
    
    issues = []
    warnings = []
    
    # Check 1: Python version
    print("✓ Checking Python version...")
    if sys.version_info < (3, 8):
        issues.append("Python 3.8+ required")
    else:
        print(f"  Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check 2: .env file
    print("✓ Checking .env file...")
    if not os.path.exists('.env'):
        warnings.append(".env file not found - create from .env.example")
    else:
        print("  .env file found")
    
    # Check 3: API key
    print("✓ Checking GEMINI_API_KEY...")
    api_key = os.getenv('GEMINI_API_KEY', '')
    if not api_key:
        issues.append("GEMINI_API_KEY not set in environment")
    elif len(api_key) < 20:
        issues.append("GEMINI_API_KEY appears invalid (too short)")
    else:
        print(f"  API key found: {api_key[:10]}...")
    
    # Check 4: Required packages
    print("✓ Checking required packages...")
    try:
        import google.generativeai
        print("  google-generativeai installed")
    except ImportError:
        issues.append("google-generativeai not installed - run: pip install -r requirements.txt")
    
    try:
        import django
        print("  Django installed")
    except ImportError:
        issues.append("Django not installed")
    
    # Check 5: Static files
    print("✓ Checking static files...")
    if not os.path.exists('static/js/chat-widget.js'):
        issues.append("chat-widget.js not found")
    else:
        print("  chat-widget.js found")
    
    if not os.path.exists('static/css/chat-widget.css'):
        issues.append("chat-widget.css not found")
    else:
        print("  chat-widget.css found")
    
    # Check 6: AI assistant module
    print("✓ Checking AI assistant module...")
    if not os.path.exists('applications/ai_assistant.py'):
        issues.append("ai_assistant.py not found")
    else:
        print("  ai_assistant.py found")
    
    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if not issues and not warnings:
        print("✓ All checks passed! Your AI Assistant is ready to use.")
        print()
        print("Next steps:")
        print("1. Run: python manage.py runserver")
        print("2. Open: http://127.0.0.1:8000")
        print("3. Click the green chat button")
        return True
    
    if warnings:
        print()
        print("⚠ WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if issues:
        print()
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        print()
        print("Please fix these issues before using the AI Assistant.")
        return False
    
    return True

if __name__ == "__main__":
    from decouple import config
    os.environ.setdefault('GEMINI_API_KEY', config('GEMINI_API_KEY', default=''))
    check_setup()
