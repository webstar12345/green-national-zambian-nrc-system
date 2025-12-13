# Google OAuth Login Setup Guide

This guide will help you set up Google OAuth authentication for your NRC System.

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "Zambian NRC System" and click "Create"

## Step 2: Enable Google+ API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click on it and press "Enable"

## Step 3: Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Select "External" user type and click "Create"
3. Fill in the required information:
   - **App name**: Zambian NRC System
   - **User support email**: Your email
   - **Developer contact email**: Your email
4. Click "Save and Continue"
5. On "Scopes" page, click "Save and Continue" (default scopes are fine)
6. On "Test users" page, add your email for testing
7. Click "Save and Continue"

## Step 4: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Select "Web application"
4. Name it "NRC System Web Client"
5. Add Authorized JavaScript origins:
   ```
   http://localhost:8000
   https://nrccard.onrender.com
   ```
6. Add Authorized redirect URIs:
   ```
   http://localhost:8000/accounts/google/login/callback/
   https://nrccard.onrender.com/accounts/google/login/callback/
   ```
7. Click "Create"
8. **IMPORTANT**: Copy your Client ID and Client Secret

## Step 5: Update Environment Variables

### For Local Development (.env file):
```env
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here
```

### For Production (Render.com):
1. Go to your Render dashboard
2. Select your web service
3. Go to "Environment" tab
4. Add these environment variables:
   - `GOOGLE_CLIENT_ID`: Your Google Client ID
   - `GOOGLE_CLIENT_SECRET`: Your Google Client Secret
5. Click "Save Changes"

## Step 6: Run Database Migrations

After deploying, run these commands:

```bash
# Local development
python manage.py migrate

# Or if already deployed, Render will run migrations automatically
```

## Step 7: Configure Social Application in Django Admin

### Option A: Using Django Admin (Recommended)

1. Go to your admin panel: https://nrccard.onrender.com/admin/
2. Login with your admin credentials
3. Under "Sites", click "Sites"
4. Edit the existing site:
   - Domain name: `nrccard.onrender.com`
   - Display name: `Zambian NRC System`
5. Under "Social Applications", click "Add Social Application"
6. Fill in:
   - **Provider**: Google
   - **Name**: Google OAuth
   - **Client id**: Your Google Client ID
   - **Secret key**: Your Google Client Secret
   - **Sites**: Select "Zambian NRC System" and move it to "Chosen sites"
7. Click "Save"

### Option B: Using Management Command

Create a file `accounts/management/commands/setup_google_oauth.py`:

```python
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from decouple import config

class Command(BaseCommand):
    help = 'Setup Google OAuth configuration'

    def handle(self, *args, **options):
        # Get or create site
        site = Site.objects.get_current()
        site.domain = config('SITE_DOMAIN', default='nrccard.onrender.com')
        site.name = 'Zambian NRC System'
        site.save()

        # Create or update Google social app
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': config('GOOGLE_CLIENT_ID', default=''),
                'secret': config('GOOGLE_CLIENT_SECRET', default=''),
            }
        )
        
        if not created:
            google_app.client_id = config('GOOGLE_CLIENT_ID', default='')
            google_app.secret = config('GOOGLE_CLIENT_SECRET', default='')
            google_app.save()
        
        google_app.sites.add(site)
        
        self.stdout.write(self.style.SUCCESS('Google OAuth configured successfully!'))
```

Then run:
```bash
python manage.py setup_google_oauth
```

## Step 8: Test Google Login

1. Visit your login page: https://nrccard.onrender.com/accounts/login/
2. Click "Sign in with Google"
3. Select your Google account
4. Grant permissions
5. You should be redirected back and logged in!

## Troubleshooting

### Error: "redirect_uri_mismatch"
- Make sure your redirect URI in Google Console exactly matches:
  `https://nrccard.onrender.com/accounts/google/login/callback/`
- Check for trailing slashes

### Error: "Social application not found"
- Make sure you've configured the Social Application in Django admin
- Verify the Client ID and Secret are correct

### Users can't sign up with Google
- Check that `SOCIALACCOUNT_AUTO_SIGNUP = True` in settings.py
- Verify email verification is set to 'optional' or 'none'

### Google button doesn't appear
- Make sure django-allauth is installed: `pip install django-allauth`
- Check that templates are loading the socialaccount tags: `{% load socialaccount %}`

## Security Notes

- Never commit your Client Secret to Git
- Use environment variables for all sensitive data
- In production, always use HTTPS
- Regularly rotate your OAuth credentials
- Monitor OAuth usage in Google Cloud Console

## Additional Features

### Get User's Google Profile Picture

In your user model or profile, you can access Google profile data:

```python
from allauth.socialaccount.models import SocialAccount

def get_google_avatar(user):
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        return social_account.extra_data.get('picture', None)
    except SocialAccount.DoesNotExist:
        return None
```

### Disconnect Google Account

Users can disconnect their Google account from their profile page by going to:
`/accounts/social/connections/`

## Support

If you encounter issues:
1. Check Django logs for detailed error messages
2. Verify all environment variables are set correctly
3. Ensure Google Cloud Console settings match your configuration
4. Test with a fresh incognito/private browser window

---

**Your NRC System now supports Google OAuth login! 🎉**
