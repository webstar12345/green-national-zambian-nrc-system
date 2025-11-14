# AI Assistant Setup Guide

This guide will help you set up the multilingual AI assistant powered by Google Gemini.

## Prerequisites

1. Python 3.8 or higher installed
2. Django project set up and running
3. Google account for API access

## Step 1: Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

## Step 2: Configure Environment Variables

1. Create a `.env` file in your project root (if it doesn't exist):
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and add your API key:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```

3. Save the file

## Step 3: Install Dependencies

Run the following command to install the required package:

```bash
pip install google-generativeai==0.3.1
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

## Step 4: Test the Setup

Run the test script to verify everything is working:

```bash
python test_ai_assistant.py
```

You should see output like:
```
Testing NRC AI Assistant...
--------------------------------------------------
✓ API Key found: AIzaSyB...
Testing English Assistant:
✓ Response: For a new NRC application, you will need...
Testing Bemba Assistant:
✓ Response: Ukwapplya sha NRC impya...
--------------------------------------------------
✓ All tests passed! AI Assistant is working correctly.
```

## Step 5: Start the Server

Start your Django development server:

```bash
python manage.py runserver
```

## Step 6: Use the AI Assistant

1. Open your browser and go to http://127.0.0.1:8000
2. Log in to your account
3. Look for the green chat button in the bottom-right corner
4. Click it to open the chat widget
5. Select your preferred language from the dropdown
6. Start chatting!

## Supported Languages

The AI assistant supports the following languages:

- **English** (en): Default language
- **Bemba** (bem): One of Zambia's major languages
- **Nyanja** (nya): Widely spoken in Eastern Zambia
- **Tonga** (toi): Spoken in Southern Zambia
- **Lozi** (loz): Spoken in Western Zambia

## Features

### Quick Responses
Click on suggested questions to get instant answers:
- How do I apply for a new NRC?
- What documents do I need?
- How long does processing take?
- How do I replace a lost NRC?

### Language Switching
You can switch languages at any time during the conversation using the language selector in the chat header.

### Context-Aware
The assistant understands the context of your questions and provides relevant information about:
- NRC application requirements
- Document requirements
- Application process steps
- System navigation help

## Troubleshooting

### Issue: "API Key not found"
**Solution**: Make sure you've created a `.env` file and added your `GEMINI_API_KEY`

### Issue: "Invalid API Key"
**Solution**: 
1. Verify your API key is correct
2. Check if the API key has proper permissions
3. Generate a new API key if needed

### Issue: Chat widget not appearing
**Solution**:
1. Make sure you're logged in
2. Clear your browser cache
3. Check browser console for JavaScript errors
4. Verify static files are loaded correctly

### Issue: Slow responses
**Solution**:
1. Check your internet connection
2. Gemini API might be experiencing high traffic
3. Try again after a few moments

### Issue: Chat not responding
**Solution**:
1. Check if the Django server is running
2. Verify the API key is valid
3. Check server logs for errors
4. Ensure the `/api/chat/` endpoint is accessible

## API Rate Limits

Google Gemini API has rate limits:
- Free tier: 60 requests per minute
- If you exceed limits, you'll need to wait or upgrade your plan

## Security Notes

1. **Never commit your `.env` file** to version control
2. Keep your API key secret
3. Use environment variables for production
4. Consider implementing rate limiting for production use
5. Monitor API usage to avoid unexpected charges

## Production Deployment

For production deployment:

1. Set environment variables on your server:
   ```bash
   export GEMINI_API_KEY=your-api-key-here
   ```

2. Or use your hosting platform's environment variable settings

3. Consider implementing:
   - Request caching to reduce API calls
   - Rate limiting per user
   - Error handling and fallback responses
   - Conversation history storage

## Cost Considerations

- Gemini API offers a free tier with generous limits
- Monitor your usage at [Google AI Studio](https://makersuite.google.com/)
- Consider implementing caching for common questions
- Set up usage alerts to avoid unexpected charges

## Support

If you encounter issues:

1. Check the [Google AI Documentation](https://ai.google.dev/docs)
2. Review Django logs for errors
3. Test the API key with the test script
4. Check browser console for frontend errors

## Additional Resources

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Django Documentation](https://docs.djangoproject.com/)
- [Project README](README.md)

---

**Happy chatting! 🤖💬**
