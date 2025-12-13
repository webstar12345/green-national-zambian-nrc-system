"""
Test script for AI Assistant
Run this to verify your Gemini API key is working
"""
import os
from applications.ai_assistant import NRCAssistant

def test_assistant():
    from decouple import config
    print("Testing NRC AI Assistant...")
    print("-" * 50)
    
    # Check if API key is set
    api_key = config('GEMINI_API_KEY', default='')
    if not api_key or api_key == 'your-gemini-api-key-here':
        print("❌ ERROR: GEMINI_API_KEY not found in environment variables")
        print("Please set your API key in .env file")
        return False
    
    print(f"✓ API Key found: {api_key[:10]}...")
    print()
    
    # Test English assistant
    print("Testing English Assistant:")
    assistant_en = NRCAssistant(language='en')
    response = assistant_en.send_message("What documents do I need for a new NRC?")
    
    if response['success']:
        print(f"✓ Response: {response['message'][:100]}...")
    else:
        print(f"❌ Error: {response['message']}")
        return False
    
    print()
    
    # Test Bemba assistant
    print("Testing Bemba Assistant:")
    assistant_bem = NRCAssistant(language='bem')
    response = assistant_bem.send_message("Nshili apply sha NRC impya?")
    
    if response['success']:
        print(f"✓ Response: {response['message'][:100]}...")
    else:
        print(f"❌ Error: {response['message']}")
        return False
    
    print()
    print("-" * 50)
    print("✓ All tests passed! AI Assistant is working correctly.")
    return True

if __name__ == "__main__":
    import django
    from decouple import config
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nrc_system.settings')
    os.environ.setdefault('GEMINI_API_KEY', config('GEMINI_API_KEY', default=''))
    django.setup()
    
    test_assistant()
