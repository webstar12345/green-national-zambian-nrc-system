# Cloudinary Setup Guide - Fix Disappearing Profile Images

## 🔴 The Problem

On Render's free tier, uploaded files (like profile images) **disappear after server restarts** because Render uses an **ephemeral filesystem**. Files are stored temporarily and deleted when the server restarts.

## ✅ The Solution: Cloudinary

Cloudinary provides **permanent cloud storage** for images. Once uploaded, images stay forever and load faster with CDN.

## 📝 Step-by-Step Setup

### 1. Create Cloudinary Account (FREE)

1. Go to: https://cloudinary.com/users/register/free
2. Sign up with your email
3. Verify your email
4. Login to your dashboard

### 2. Get Your Credentials

Once logged in, you'll see your **Dashboard**:

```
Cloud name: your-cloud-name
API Key: 123456789012345
API Secret: abcdefghijklmnopqrstuvwxyz
```

**Copy these three values!**

### 3. Add to Render Environment Variables

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your **nrccard** service
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Add these **4 variables**:

```
USE_CLOUDINARY = True
CLOUDINARY_CLOUD_NAME = your-cloud-name
CLOUDINARY_API_KEY = 123456789012345
CLOUDINARY_API_SECRET = abcdefghijklmnopqrstuvwxyz
```

**Important:** Replace with YOUR actual values from Cloudinary dashboard!

### 4. Deploy the Changes

The code is already updated. Just deploy:

```bash
git add requirements.txt nrc_system/settings.py .env.example
git commit -m "Add Cloudinary for permanent image storage"
git push origin main
```

Render will automatically rebuild with Cloudinary support.

### 5. Test It!

1. Wait for Render to finish deploying (2-3 minutes)
2. Go to your profile
3. Upload a profile image
4. Save
5. Refresh the page - **image should still be there!**
6. Wait a few hours and check again - **still there!**

## 🎯 What This Fixes

### Before (Without Cloudinary):
- ❌ Upload profile image
- ❌ Image shows temporarily
- ❌ Server restarts (happens frequently on free tier)
- ❌ Image disappears
- ❌ User frustrated

### After (With Cloudinary):
- ✅ Upload profile image
- ✅ Image stored on Cloudinary cloud
- ✅ Server restarts (no problem!)
- ✅ Image still there
- ✅ Loads faster with CDN
- ✅ User happy!

## 📊 Cloudinary Free Tier Limits

Perfect for your NRC system:

- **Storage:** 25 GB
- **Bandwidth:** 25 GB/month
- **Transformations:** 25,000/month
- **Images:** Unlimited

This is enough for **thousands of users**!

## 🔧 How It Works

### Before:
```
User uploads image → Saved to Render server → Server restarts → Image deleted
```

### After:
```
User uploads image → Uploaded to Cloudinary → Stored permanently → Always available
```

## 🌐 Additional Benefits

1. **CDN Delivery** - Images load faster worldwide
2. **Automatic Optimization** - Images compressed automatically
3. **Transformations** - Can resize/crop images on-the-fly
4. **Backup** - Images backed up automatically
5. **No Server Load** - Images served from Cloudinary, not your server

## 📱 What Gets Stored on Cloudinary

- ✅ Profile images
- ✅ NRC application photos
- ✅ Document uploads
- ✅ Any user-uploaded files

## 🔒 Security

- ✅ Secure HTTPS delivery
- ✅ Access control
- ✅ API authentication
- ✅ Private uploads option

## 🐛 Troubleshooting

### Images Still Disappearing?

1. **Check Environment Variables**
   - Go to Render dashboard
   - Verify all 4 Cloudinary variables are set
   - Make sure `USE_CLOUDINARY=True`

2. **Check Cloudinary Dashboard**
   - Login to Cloudinary
   - Go to Media Library
   - See if images are being uploaded

3. **Check Logs**
   - In Render dashboard, check logs
   - Look for Cloudinary errors

### Can't Upload Images?

1. **Check Credentials**
   - Make sure API Key and Secret are correct
   - No extra spaces in environment variables

2. **Check Cloudinary Quota**
   - Login to Cloudinary
   - Check if you've hit free tier limits

## 💰 Cost

**FREE** for your use case!

The free tier is more than enough for:
- Small to medium applications
- Thousands of users
- Hundreds of images per day

## 🔄 Migration

### Existing Images

Old images stored on Render are already gone (ephemeral filesystem). Users will need to re-upload their profile images once.

### New Images

All new uploads will go directly to Cloudinary and stay forever!

## 📞 Support

If you have issues:

1. **Cloudinary Support:** https://support.cloudinary.com
2. **Documentation:** https://cloudinary.com/documentation
3. **Community:** https://community.cloudinary.com

## ✅ Checklist

- [ ] Created Cloudinary account
- [ ] Got Cloud Name, API Key, API Secret
- [ ] Added 4 environment variables to Render
- [ ] Deployed code changes
- [ ] Tested profile image upload
- [ ] Verified image persists after refresh
- [ ] Checked Cloudinary Media Library

## 🎉 Done!

Your profile images will now **never disappear** again! They're stored permanently on Cloudinary's cloud infrastructure.

---

**Next Steps:**
1. Set up Cloudinary account (5 minutes)
2. Add environment variables to Render (2 minutes)
3. Deploy (automatic)
4. Test and enjoy permanent images! 🎊
