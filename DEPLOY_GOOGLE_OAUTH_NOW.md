# Deploy Google OAuth NOW - Simple Steps

## Step 1: Deploy Code (30 seconds)

Run these commands in Git Bash:

```bash
git add .
git commit -m "Add Google OAuth login"
git push origin main
```

Wait 2-3 minutes for Render to deploy.

## Step 2: Google Cloud Console (3 minutes)

1. Go to: https://console.cloud.google.com/
2. Click "New Project" → Name: "Zambian NRC System"
3. Go to "APIs & Services" → "Library" → Enable "Google+ API"
4. Go to "OAuth consent screen":
   - External → Fill app name → Add your email → Save
5. Go to "Credentials" → "Create OAuth Client ID":
   - Web application
   - Add redirect URI: `https://nrccard.onrender.com/accounts/google/login/callback/`
   - Create
6. **COPY** the Client ID and Client Secret

## Step 3: Add to Render (1 minute)

1. Go to: https://dashboard.render.com/
2. Select your "nrccard" service
3. Click "Environment" tab
4. Add these variables:
   - Key: `GOOGLE_CLIENT_ID` → Value: (paste Client ID)
   - Key: `GOOGLE_CLIENT_SECRET` → Value: (paste Client Secret)
   - Key: `SITE_DOMAIN` → Value: `nrccard.onrender.com`
5. Click "Save Changes"

## Step 4: Configure in Admin (1 minute)

1. Go to: https://nrccard.onrender.com/admin/
2. Login with admin credentials
3. Click "Sites" → Edit the site:
   - Domain: `nrccard.onrender.com`
   - Name: `Zambian NRC System`
   - Save
4. Click "Social applications" → "Add social application":
   - Provider: Google
   - Name: Google OAuth
   - Client id: (paste your Client ID)
   - Secret key: (paste your Client Secret)
   - Sites: Move "Zambian NRC System" to "Chosen sites"
   - Save

## Step 5: Test! (30 seconds)

1. Go to: https://nrccard.onrender.com/accounts/login/
2. You should see "Sign in with Google" button
3. Click it and test login!

## Done! 🎉

Your users can now sign in with Google in one click!

---

**Total time: ~6 minutes**

**Need help?** See GOOGLE_OAUTH_SETUP.md for detailed troubleshooting.
