# Google OAuth Flow Diagram

## Visual Flow

```
┌─────────────┐
│    USER     │
└──────┬──────┘
       │
       │ 1. Clicks "Sign in with Google"
       ▼
┌─────────────────────┐
│   NRC Login Page    │
│  /accounts/login/   │
└──────┬──────────────┘
       │
       │ 2. Redirects to Google
       ▼
┌─────────────────────┐
│   Google Login      │
│  accounts.google    │
└──────┬──────────────┘
       │
       │ 3. User authenticates
       │    with Google
       ▼
┌─────────────────────┐
│  Google OAuth       │
│  Authorization      │
└──────┬──────────────┘
       │
       │ 4. Redirects back with code
       ▼
┌─────────────────────────────────┐
│   OAuth Callback                │
│   /accounts/google/login/       │
│   callback/                     │
└──────┬──────────────────────────┘
       │
       │ 5. Exchange code for token
       ▼
┌─────────────────────┐
│  Django Allauth     │
│  - Get user info    │
│  - Create account   │
│  - Login user       │
└──────┬──────────────┘
       │
       │ 6. Redirect to home
       ▼
┌─────────────────────┐
│   NRC Home Page     │
│   User logged in!   │
└─────────────────────┘
```

## Step-by-Step Explanation

### Step 1: User Clicks Button
- User visits `/accounts/login/`
- Sees "Sign in with Google" button
- Clicks the button

### Step 2: Redirect to Google
- Django generates OAuth URL
- Includes client_id, redirect_uri, scope
- Adds state parameter for security
- Redirects user to Google

### Step 3: Google Authentication
- User sees Google login page
- Enters Google credentials
- Grants permissions to app
- Google validates user

### Step 4: Callback with Code
- Google redirects back to your site
- URL: `/accounts/google/login/callback/`
- Includes authorization code
- Includes state parameter

### Step 5: Token Exchange
- Django sends code to Google
- Includes client_secret
- Google returns access token
- Django gets user profile info

### Step 6: Account Creation/Login
- Django-allauth checks if user exists
- Creates new user if needed
- Links Google account to user
- Logs user in
- Redirects to home page

## Security Features

```
┌─────────────────────────────────┐
│   Security Measures             │
├─────────────────────────────────┤
│ ✓ HTTPS required                │
│ ✓ State parameter (CSRF)        │
│ ✓ Client secret never exposed   │
│ ✓ Short-lived auth codes        │
│ ✓ Token stored securely         │
│ ✓ Scope limited to profile      │
└─────────────────────────────────┘
```

## Data Flow

```
Google Profile Data
        │
        ▼
┌─────────────────┐
│   Email         │──────┐
│   First Name    │      │
│   Last Name     │      │
│   Profile Pic   │      │
└─────────────────┘      │
                         │
                         ▼
                  ┌──────────────┐
                  │  Django User │
                  │  - username  │
                  │  - email     │
                  │  - name      │
                  └──────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Social       │
                  │ Account      │
                  │ - provider   │
                  │ - uid        │
                  │ - token      │
                  └──────────────┘
```

## Database Changes

```
Before Login:
┌──────────────┐
│   No User    │
└──────────────┘

After Google Login:
┌──────────────────────────────┐
│   User Table                 │
│   - id: 1                    │
│   - username: john_doe       │
│   - email: john@gmail.com    │
│   - first_name: John         │
│   - last_name: Doe           │
└──────────────────────────────┘
         │
         │ linked to
         ▼
┌──────────────────────────────┐
│   SocialAccount Table        │
│   - user_id: 1               │
│   - provider: google         │
│   - uid: 123456789           │
│   - extra_data: {...}        │
└──────────────────────────────┘
```

## Configuration Flow

```
1. Google Cloud Console
   ↓
   Creates OAuth App
   ↓
   Generates Client ID & Secret
   ↓
2. Render Environment
   ↓
   Stores credentials
   ↓
3. Django Settings
   ↓
   Configures allauth
   ↓
4. Django Admin
   ↓
   Creates SocialApp
   ↓
5. Ready to Use!
```

## Error Handling

```
┌─────────────────────┐
│   User clicks       │
│   Google login      │
└──────┬──────────────┘
       │
       ▼
   ┌───────┐
   │ Error?│
   └───┬───┘
       │
   ┌───┴───┐
   │  Yes  │  No
   │       │
   ▼       ▼
┌──────┐ ┌──────┐
│Show  │ │Login │
│Error │ │User  │
└──────┘ └──────┘
```

## Common Errors

```
redirect_uri_mismatch
    ↓
Check Google Console
    ↓
Verify redirect URI matches exactly

Social app not found
    ↓
Check Django Admin
    ↓
Create SocialApp with credentials

Invalid client
    ↓
Check environment variables
    ↓
Verify Client ID and Secret
```

## Success Path

```
User → Click → Google → Auth → Callback → Create → Login → Home
  ✓      ✓       ✓       ✓       ✓         ✓       ✓      ✓
```

---

**This flow ensures secure, seamless authentication! 🔒**
