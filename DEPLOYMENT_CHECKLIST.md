# Deployment Checklist

## Pre-Deployment

- [ ] All features tested locally
- [ ] Database migrations created
- [ ] Static files working
- [ ] Media uploads working
- [ ] Password reset tested
- [ ] AI assistant tested
- [ ] Admin panel accessible

## GitHub Setup

- [ ] Create GitHub repository
- [ ] Initialize git in project
- [ ] Add all files to git
- [ ] Commit changes
- [ ] Push to GitHub

## Render Account

- [ ] Create Render account
- [ ] Connect GitHub account
- [ ] Verify email

## Database Setup

- [ ] Create PostgreSQL database
- [ ] Copy Internal Database URL
- [ ] Save URL securely

## Web Service Setup

- [ ] Create new web service
- [ ] Connect GitHub repository
- [ ] Configure build command
- [ ] Configure start command
- [ ] Add environment variables:
  - [ ] SECRET_KEY
  - [ ] DEBUG=False
  - [ ] DATABASE_URL
  - [ ] ALLOWED_HOSTS
  - [ ] GEMINI_API_KEY
- [ ] Deploy service

## Post-Deployment

- [ ] Wait for deployment to complete
- [ ] Check logs for errors
- [ ] Create superuser account
- [ ] Test website access
- [ ] Test login/signup
- [ ] Test NRC application
- [ ] Test admin panel
- [ ] Test password reset
- [ ] Test AI assistant

## Optional Configuration

- [ ] Add custom domain
- [ ] Configure email settings
- [ ] Set up monitoring
- [ ] Enable backups
- [ ] Add SSL certificate (automatic)

## Final Checks

- [ ] All pages load correctly
- [ ] Static files display
- [ ] Images upload successfully
- [ ] Forms submit properly
- [ ] Database saves data
- [ ] Admin can manage applications
- [ ] Users can apply for NRC
- [ ] Password reset works
- [ ] AI chat responds

## Documentation

- [ ] Update README with live URL
- [ ] Document admin credentials (securely)
- [ ] Create user guide
- [ ] Train administrators

---

**Once all items are checked, your system is ready for production use!** ✅
