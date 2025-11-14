# Quick Start: AI Assistant

Get up and running with the multilingual AI assistant in 5 minutes!

## 🚀 Quick Setup

### 1. Get API Key (2 minutes)
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

### 2. Configure (1 minute)
```bash
# Create .env file
echo GEMINI_API_KEY=your-api-key-here > .env
```

### 3. Install & Run (2 minutes)
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python manage.py runserver
```

## ✅ Test It

1. Open http://127.0.0.1:8000
2. Login to your account
3. Click the green chat button (bottom-right)
4. Ask: "What documents do I need?"

## 🌍 Supported Languages

| Language | Code | Example Question |
|----------|------|------------------|
| English  | en   | "How do I apply for a new NRC?" |
| Bemba    | bem  | "Nshili apply sha NRC impya?" |
| Nyanja   | nya  | "Ndingapange bwanji application?" |
| Tonga    | toi  | "Ndili apply buti NRC mpya?" |
| Lozi     | loz  | "Ke ka etsa jwang application?" |

## 💡 Quick Tips

- **Switch Languages**: Use the dropdown in chat header
- **Quick Responses**: Click suggested questions
- **Context-Aware**: Ask follow-up questions
- **Always Available**: Works 24/7

## 🔧 Troubleshooting

**Chat not appearing?**
- Make sure you're logged in
- Check if static files are loaded
- Clear browser cache

**API errors?**
- Verify API key in `.env`
- Check internet connection
- Ensure API key is valid

## 📚 More Help

- Full setup guide: `AI_ASSISTANT_SETUP.md`
- Demo page: http://127.0.0.1:8000/ai-demo/
- Test script: `python test_ai_assistant.py`

---

**Ready to chat? Click the green button! 💬**
