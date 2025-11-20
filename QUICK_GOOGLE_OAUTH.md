# Quick Google OAuth Setup (5 Minutes)

## 1. Google Cloud Console Setup (2 minutes)

1. Go to https://console.cloud.google.com/
2. Create new project: "Zambian NRC System"
3. Enable "Google+ API" from APIs & Services → Library
4. Go to OAuth consent screen:
   - User type: External
   - App name: Zambian NRC System
   - Add your email
   - Save
5. Go to Credentials → Create OAuth Client ID:
   - Type: Web application
   - Authorized redirect URIs:
     ```
     http://localhost:8000/accounts/google/login/callback/
     https://nrccard.onrender.com/accounts/google/login/callback/
     ```
   - Copy Client ID and Client Secret

## 2. Add to Render Environment (1 minute)

1. Go to Render dashboard → Your service → Environment
2. Add:
   - `GOOGLE_CLIENT_ID` = (paste your Client ID)
   - `GOOGLE_CLIENT_SECRET` = (paste your Client Secret)
3. Save Changes

## 3. Deploy (1 minute)

Run in your terminal:
```bash
git add .
git commit -m "Add Google OAuth login"
git push origin main
```

## 4. Configure in Admin (1 minute)

After deployment:
1. Go to https://nrccard.onrender.com/admin/
2. Under "Social Applications" → Add
3. Fill in:
   - Provider: Google
   - Name: Google OAuth
   - Client ID: (your Client ID)
   - Secret: (your Client Secret)
   - Sites: Select "Zambian NRC System"
4. Save

## Done! 🎉

Test at: https://nrccard.onrender.com/accounts/login/

You should see a "Sign in with Google" button!

---

**Need help?** See full guide: GOOGLE_OAUTH_SETUP.md
