# Render Deployment Setup Guide

## Required Environment Variables

Set these in your Render dashboard (Settings > Environment):

### Core Django Settings
```
DEBUG=False
SECRET_KEY=your-secret-key-here  # Generate a secure key
ALLOWED_HOSTS=fleeting-logistics-ynzx.onrender.com,www.fleeting-logistics-ynzx.onrender.com
```

### Email Configuration (Gmail/SMTP)
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password  # Use App Password, not regular password
DEFAULT_FROM_EMAIL=your-email@gmail.com
ADMIN_EMAIL=your-email@gmail.com
```

### Database
Render SQLite should work automatically, but ensure the build script runs migrations.

## Deployment Steps

1. **Set Environment Variables** in Render Dashboard:
   - Go to Settings → Environment
   - Add all variables from above
   - Save

2. **Clear Build Cache** (if redeploying):
   - Go to Settings → Build & Deploy
   - Click "Clear build cache"
   - Click "Deploy"

3. **Verify Deployment**:
   - Check deployment logs for errors
   - Visit https://your-domain.onrender.com/
   - Test signup at https://your-domain.onrender.com/accounts/signup/

## Troubleshooting

### 500 Error on Signup
- Check if EMAIL configuration is set
- Ensure DEBUG=False or DEBUG=True for testing
- Check Render logs for stack trace

### Static Files Not Loading
- Run: `python manage.py collectstatic --noinput`
- Verify STATIC_ROOT and STATICFILES_DIRS in settings

### Database Errors
- Check if migrations ran: `python manage.py showmigrations`
- Manual fix: SSH into Render service and run migrations

## Production Checklist

- [ ] All environment variables configured
- [ ] DEBUG=False for security
- [ ] SECRET_KEY is random and secure
- [ ] Email credentials configured
- [ ] Database migrated
- [ ] Static files collected
- [ ] ALLOWED_HOSTS includes your domain
