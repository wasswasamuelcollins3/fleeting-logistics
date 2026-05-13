# 🚀 Deployment Guide - Render.com

## Prerequisites
- GitHub repository with your code
- Render.com account

## Step 1: Set Up Environment Variables on Render

Go to your Render service dashboard and add these environment variables:

```
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here
ALLOWED_HOSTS=your-app-name.onrender.com,www.your-domain.com
DATABASE_URL=postgresql://username:password@your-db-host:5432/db_name
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@fleetinglogistics.com
ADMIN_EMAIL=info@fleetinglogistics.com
```

### Generate a Strong SECRET_KEY
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Step 2: Connect GitHub Repository

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Select the main branch
4. Choose Python 3.12.7 runtime

## Step 3: Configure Build & Start Commands

**Build Command:**
```bash
python -m pip install --upgrade pip && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

**Start Command:**
```bash
gunicorn fleeting_logistics.wsgi:application
```

## Step 4: Add PostgreSQL Database (Optional)

For production, use PostgreSQL instead of SQLite:

1. Create a PostgreSQL database on Render
2. Copy the connection string
3. Set `DATABASE_URL` to the full connection string from Render (settings parse it with **dj-database-url**).

## Step 5: Deploy

1. Push your code to GitHub
2. Render will automatically build and deploy
3. Check the deploy logs for any errors

## Troubleshooting

### Build fails with package errors
- Clear build cache and redeploy
- Check requirements.txt compatibility

### Gunicorn exits with status 1
- Check Django logs in Render dashboard
- Verify all environment variables are set
- Ensure database connection string is correct

### Static files not loading
- Run `python manage.py collectstatic --noinput`
- Ensure STATIC_ROOT is set correctly

### Database errors
- Check DATABASE_URL format
- Verify database exists and is accessible
- Run migrations manually: `python manage.py migrate`

## Production Checklist

- [ ] DEBUG=False
- [ ] SECRET_KEY is strong and unique
- [ ] ALLOWED_HOSTS includes your domain
- [ ] Database is PostgreSQL (not SQLite)
- [ ] Email configuration is correct
- [ ] Static files are collected
- [ ] HTTPS is enabled
- [ ] Environment variables are set in Render dashboard

## Support

For more help:
- [Render Documentation](https://render.com/docs)
- [Django Deployment Guide](https://docs.djangoproject.com/en/6.0/howto/deployment/)
