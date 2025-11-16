# 🔑 Gemini API Key Setup Guide

Follow these steps to enable full AI capabilities for your NRC Assistant.

---

## 📋 **Step 1: Get Your Free Gemini API Key**

### **Option A: Google AI Studio (Recommended)**

1. **Visit:** https://aistudio.google.com/app/apikey
2. **Sign in** with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Click **"Create API key in new project"** (or select existing project)
5. **Copy the API key** (it looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`)
6. **Save it securely** - you'll need it in the next step

### **Option B: Google Cloud Console**

1. Go to: https://console.cloud.google.com/
2. Create a new project or select existing one
3. Enable **"Generative Language API"**
4. Go to **"Credentials"** → **"Create Credentials"** → **"API Key"**
5. Copy the generated API key

---

## 🚀 **Step 2: Add API Key to Render**

### **On Render Dashboard:**

1. **Go to:** https://dashboard.render.com
2. **Click** on your web service: `green-national-zambian-nrc-system`
3. **Click** "Environment" tab (left sidebar)
4. **Click** "Add Environment Variable"
5. **Add the following:**
   - **Key:** `GEMINI_API_KEY`
   - **Value:** Paste your API key (e.g., `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`)
6. **Click** "Save Changes"

### **Render will automatically:**
- Detect the new environment variable
- Trigger a redeploy
- Your AI will start using Gemini API

---

## ✅ **Step 3: Verify It's Working**

After deployment completes (2-3 minutes):

1. **Open your site**
2. **Login** to your account
3. **Open the chat widget** (bottom right)
4. **Ask a question:** "How do I apply for an NRC?"
5. **You should get** a detailed AI-powered response!

---

## 🆓 **Gemini API Free Tier**

### **What You Get Free:**
- **60 requests per minute**
- **1,500 requests per day**
- **1 million tokens per month**
- **No credit card required**

### **Perfect For:**
- Small to medium websites
- Testing and development
- Personal projects
- Educational use

---

## 🔐 **Security Best Practices**

### **DO:**
✅ Keep your API key secret
✅ Only add it to Render environment variables
✅ Never commit it to GitHub
✅ Rotate keys periodically
✅ Monitor usage in Google AI Studio

### **DON'T:**
❌ Share your API key publicly
❌ Commit it to version control
❌ Hardcode it in your code
❌ Use it in client-side JavaScript
❌ Share screenshots with the key visible

---

## 📊 **Monitor Your Usage**

### **Check Usage:**
1. Go to: https://aistudio.google.com/app/apikey
2. Click on your API key
3. View usage statistics
4. Set up alerts if needed

### **Rate Limits:**
- Free tier: 60 requests/minute
- If exceeded, requests will fail
- Consider upgrading for high traffic

---

## 🔄 **What Changes After Adding API Key**

### **Before (Fallback Mode):**
- Keyword-based responses
- Predefined answers
- Limited conversation
- Basic help

### **After (Full AI Mode):**
- Natural language understanding
- Context-aware responses
- Conversational AI
- Detailed explanations
- Multi-turn conversations
- Personalized help

---

## 🧪 **Test Questions**

Try these to see the difference:

**Simple Questions:**
- "How do I apply for an NRC?"
- "What documents do I need?"

**Complex Questions:**
- "I lost my NRC 2 years ago and never reported it. What should I do now?"
- "Can I apply for my child who is 15 years old?"
- "What's the difference between new application and replacement?"

**Conversational:**
- "Hello, I need help"
- "Can you explain the process step by step?"
- "What happens after I submit my application?"

---

## ⚠️ **Troubleshooting**

### **API Key Not Working:**

1. **Check the key is correct:**
   - No extra spaces
   - Complete key copied
   - Starts with `AIzaSy`

2. **Verify API is enabled:**
   - Go to Google Cloud Console
   - Check "Generative Language API" is enabled

3. **Check Render logs:**
   - Look for API errors
   - Verify environment variable is set

4. **Test locally first:**
   - Add key to your `.env` file
   - Run: `python manage.py runserver`
   - Test the chat widget

### **Rate Limit Errors:**

If you see "quota exceeded" errors:
- You've hit the free tier limit
- Wait for the limit to reset (1 minute or 1 day)
- Consider upgrading to paid tier
- Implement caching for common questions

### **API Errors:**

Common errors and solutions:
- `API key not valid` → Check key is correct
- `API not enabled` → Enable Generative Language API
- `Quota exceeded` → Wait or upgrade
- `Invalid request` → Check code is up to date

---

## 💰 **Upgrading (Optional)**

If you need more capacity:

1. **Go to:** https://console.cloud.google.com/billing
2. **Enable billing** on your project
3. **Pricing:**
   - Pay-as-you-go
   - Very affordable
   - Only pay for what you use

---

## 📞 **Support**

### **Need Help?**

- **Gemini API Docs:** https://ai.google.dev/docs
- **Google AI Studio:** https://aistudio.google.com
- **Community:** https://discuss.ai.google.dev

---

## 🎉 **You're All Set!**

Once you add the API key to Render:
1. Wait 2-3 minutes for deployment
2. Test the chat widget
3. Enjoy full AI-powered assistance!

Your NRC Assistant will now provide intelligent, context-aware responses to help users with their applications.

---

**Questions? Check the troubleshooting section or contact support!**
