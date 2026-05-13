# Production Deployment Troubleshooting Guide

## Issue: 500 Errors in Production (Render)

### Root Causes

1. **Missing Environment Variables**: Django can't start without SECRET_KEY and other required settings
2. **Database not initialized**: Migrations may not have run properly
3. **DEBUG=False without proper configuration**: Error pages aren't detailed without DEBUG=True for testing

### Step-by-Step Fix

#### Step 1: Configure Environment Variables in Render

1. Go to https://dashboard.render.com
2. Select your service "fleeting-logistics"
3. Click on "Settings" in the left sidebar
4. Scroll to "Environment" section
5. Click "Add Environment Variable"
6. Add these variables one by one:

**Critical Variables**:
```
SECRET_KEY=your-super-secret-key-here-123-456-789
DEBUG=False
ALLOWED_HOSTS=fleeting-logistics-ynzx.onrender.com
```

**Email Configuration** (Choose one):

Option A - Gmail:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<Your Google App Password - NOT your regular password>
DEFAULT_FROM_EMAIL=your-email@gmail.com
ADMIN_EMAIL=your-email@gmail.com
```

**How to get Google App Password**:
- Go to https://myaccount.google.com/apppasswords
- Select "Mail" and "Windows Computer" (or your device)
- Google will generate a 16-character password
- Copy and paste it as EMAIL_HOST_PASSWORD

Option B - Other SMTP Provider (e.g., SendGrid, Mailgun):
```
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=<Your SendGrid API Key>
DEFAULT_FROM_EMAIL=noreply@fleetinglogistics.com
ADMIN_EMAIL=admin@fleetinglogistics.com
```

#### Step 2: Generate a Secure SECRET_KEY

Use Python to generate a secure key:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use online generator: https://djecrety.ir/

**Important**: Never share your SECRET_KEY publicly. It's like a password for your Django app.

#### Step 3: Clear Build Cache and Redeploy

1. In Render dashboard, click "Settings"
2. Scroll to "Build & Deploy"
3. Find "Clear build cache" button and click it
4. Find "Deploy" button and select "Latest commit"
5. Click "Deploy" to rebuild

#### Step 4: Monitor Deployment Logs

1. Go to "Logs" tab
2. Watch for any errors during deployment
3. Check that migrations completed successfully
4. Should see: `Your app is running at https://fleeting-logistics-ynzx.onrender.com`

#### Step 5: Test Deployment

After deployment completes:

1. Visit https://fleeting-logistics-ynzx.onrender.com/
2. Check if home page loads without errors
3. Visit https://fleeting-logistics-ynzx.onrender.com/booking/
4. Check if booking form loads
5. Visit https://fleeting-logistics-ynzx.onrender.com/accounts/signup/
6. Try creating a test account

### Verification Checklist

After deployment, verify:

- [ ] Home page loads (http status 200)
- [ ] Booking form loads with services listed
- [ ] Signup page doesn't show 500 error
- [ ] Can see Django admin at /admin/
- [ ] Static files loading (CSS/JS/images visible)
- [ ] No 404 errors in logs for static files

### If Still Getting 500 Errors

#### Option 1: Enable DEBUG for Troubleshooting

Temporarily set:
```
DEBUG=True
ALLOWED_HOSTS=*
```

This will show detailed error pages. **Remember to set DEBUG=False again after fixing!**

#### Option 2: Check Logs for Specific Errors

1. Go to "Logs" tab in Render dashboard
2. Look for Python traceback with specific error message
3. Common errors:
   - `ALLOWED_HOSTS not configured`: Add to environment
   - `SECRET_KEY not found`: Set in environment
   - `Email backend error`: Check email credentials
   - `Database error`: Run migrations manually

#### Option 3: SSH into Render Service

Advanced: SSH into the running service to run Django commands:

```bash
# SSH into service
render-cli service shell

# Run Django management commands
python manage.py migrate --check     # Check migration status
python manage.py migrate             # Apply migrations
python manage.py createsuperuser    # Create admin user
python manage.py shell              # Django interactive shell
```

### Database & Migrations

The deployment script should automatically run:
```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

If migrations failed during build:

1. Check build logs for migration errors
2. Clear build cache and redeploy
3. Or SSH into service and run migrations manually

### Common Issues & Solutions

| Error | Solution |
|-------|----------|
| SECRET_KEY is missing | Add SECRET_KEY environment variable |
| ALLOWED_HOSTS not configured | Add ALLOWED_HOSTS environment variable |
| Email configuration error | Verify EMAIL_HOST, PORT, credentials |
| Static files 404 | Run `collectstatic --noinput` in deployment |
| Database locked | Render SQLite can have concurrency issues; consider PostgreSQL |
| Module not found | Check requirements.txt has all dependencies |

### Next Phase: Production Optimization

Once deployment is working:

1. **Switch to PostgreSQL** (recommended for production):
   - Render offers free PostgreSQL tier
   - More reliable than SQLite for concurrent access
   - Better performance

2. **Configure CloudFlare** (optional):
   - Free HTTPS/CDN
   - DDoS protection
   - Domain custom configuration

3. **Set up Monitoring**:
   - Render has built-in error tracking
   - Configure email alerts for deployment failures
   - Monitor application logs

4. **Regular Backups**:
   - Render provides backup functionality
   - Consider database export regularly

---

**Support**: If you encounter specific error messages, paste the full error from logs for targeted troubleshooting.
