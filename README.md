# Fleeting Logistics - Enterprise Logistics Platform

> Professional, scalable logistics and delivery management system

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0+-darkgreen)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🎯 Overview

Fleeting Logistics is a comprehensive, production-ready logistics platform designed for professional cargo transportation and passenger services. Built with Django and modern frontend technologies, it provides real-time tracking, automated dashboards, and enterprise-grade features.

### Key Features

✅ **Real-time Shipment Tracking** - Track packages with live location updates  
✅ **Dual Dashboards** - Separate interfaces for customers and administrators  
✅ **Professional UI/UX** - Modern, responsive design optimized for all devices  
✅ **Secure Authentication** - JWT-based auth with email verification  
✅ **Advanced Analytics** - Business intelligence and reporting  
✅ **Mobile Responsive** - Perfect on phones, tablets, and desktops  
✅ **Performance Optimized** - 90+ PageSpeed score target  
✅ **Enterprise Security** - Industry-standard security practices  

---

## 📊 Project Status

| Component | Status | Progress |
|-----------|--------|----------|
| Core Framework | ✅ Complete | 100% |
| UI/UX Design System | ✅ Complete | 100% |
| Navigation & Layout | 🔄 In Progress | 80% |
| Authentication System | 🔄 In Progress | 60% |
| Database Models | 🔄 In Progress | 70% |
| Customer Dashboard | ⏳ Planned | 0% |
| Admin Dashboard | ⏳ Planned | 0% |
| Shipment Tracking | ⏳ Planned | 0% |
| Performance Optimization | ⏳ Planned | 0% |
| Deployment Setup | ⏳ Planned | 0% |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Node.js 16+ (optional, for frontend tools)
- Git

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/fleeting-logistics.git
cd fleeting-logistics
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Configure Database**
```bash
python manage.py migrate
```

6. **Create Superuser**
```bash
python manage.py createsuperuser
```

7. **Collect Static Files**
```bash
python manage.py collectstatic --no-input
```

8. **Run Development Server**
```bash
python manage.py runserver
```

Visit http://localhost:8000

---

## 📁 Project Structure

```
fleeting-logistics/
├── fleeting_logistics/          # Main Django project
│   ├── settings.py             # Project settings
│   ├── urls.py                 # URL configuration
│   ├── wsgi.py                 # WSGI config
│   └── asgi.py                 # ASGI config
│
├── logistics/                   # Main app
│   ├── migrations/             # Database migrations
│   ├── models.py               # Data models
│   ├── views.py                # Views
│   ├── urls.py                 # App URLs
│   ├── admin.py                # Admin config
│   └── forms.py                # Forms
│
├── templates/                   # HTML templates
│   ├── includes/               # Template includes
│   ├── base.html               # Base template
│   ├── home.html               # Homepage
│   ├── dashboard.html          # Dashboard
│   └── ...
│
├── static/                      # Static files
│   ├── css/                    # Stylesheets
│   │   ├── modern.css          # Modern design system
│   │   ├── navbar-footer.css   # Navigation styles
│   │   └── style.css           # General styles
│   ├── js/                     # JavaScript
│   ├── img/                    # Images
│   └── fonts/                  # Web fonts
│
├── staticfiles/                # Collected static files
├── manage.py                   # Django management
├── requirements.txt            # Python dependencies
├── UPGRADE_PLAN.md            # Comprehensive upgrade plan
├── IMPLEMENTATION_GUIDE.md    # Step-by-step implementation
├── README.md                   # This file
└── .env.example               # Environment variables template
```

---

## 🛠 Technology Stack

### Backend
- **Django 6.0+** - Web framework
- **Python 3.11** - Programming language
- **PostgreSQL** - Database
- **Redis** - Caching (planned)
- **Celery** - Task queue (planned)

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **JavaScript (Vanilla)** - Interactivity
- **Font Awesome** - Icons
- **Alpine.js** - Lightweight reactivity (planned)

### DevOps & Deployment
- **Docker** - Containerization
- **Nginx** - Reverse proxy
- **Gunicorn** - WSGI server
- **GitHub Actions** - CI/CD (planned)
- **AWS/DigitalOcean** - Hosting

### Tools & Services
- **Sentry** - Error tracking
- **Google Analytics** - Analytics
- **SendGrid** - Email service
- **AWS S3** - File storage (planned)

---

## 📚 Documentation

### Core Documentation
- **[UPGRADE_PLAN.md](UPGRADE_PLAN.md)** - Comprehensive upgrade roadmap
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Step-by-step implementation
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - API reference (coming soon)
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide (coming soon)

### Key Features
- **Shipment Tracking** - Real-time package tracking
- **User Authentication** - Secure login/registration
- **Dashboards** - Customer and admin interfaces
- **Notifications** - Email/SMS alerts
- **Reporting** - Analytics and insights

---

## 🔐 Security

- ✅ HTTPS enforced
- ✅ CSRF protection
- ✅ XSS prevention
- ✅ SQL injection prevention
- ✅ Password hashing (bcrypt)
- ✅ Secure headers
- ✅ Rate limiting
- ✅ Input validation
- ✅ Environment variable secrets
- ✅ Audit logging (planned)

### Security Headers
```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
X-XSS-Protection: 1; mode=block
```

---

## ⚡ Performance

### Target Metrics
- Desktop PageSpeed: **90+**
- Mobile PageSpeed: **70+**
- First Contentful Paint: **< 1.8s**
- Largest Contentful Paint: **< 2.5s**
- Cumulative Layout Shift: **< 0.1**

### Optimization Strategies
- Image compression & WebP
- CSS/JS minification
- Lazy loading
- Database indexing
- Redis caching
- CDN for static assets
- Async task processing

---

## 📦 API Endpoints (Planned)

### Authentication
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/refresh
POST   /api/auth/logout
POST   /api/auth/forgot-password
```

### Shipments
```
GET    /api/shipments/
POST   /api/shipments/create
GET    /api/shipments/{id}/
PUT    /api/shipments/{id}/update
POST   /api/shipments/{id}/track
```

### Tracking
```
GET    /api/tracking/{tracking_id}/
GET    /api/tracking/{tracking_id}/updates/
```

### Admin
```
GET    /api/admin/dashboard/
GET    /api/admin/shipments/
PUT    /api/admin/shipments/{id}/status
```

---

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

With coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📊 Database Schema

### Core Tables
- `auth_user` - User accounts
- `logistics_userprofile` - User profiles
- `logistics_shipment` - Shipment records
- `logistics_trackingupdate` - Tracking history
- `logistics_notification` - User notifications
- `logistics_contactmessage` - Contact messages

### Relationships
```
User → UserProfile (1:1)
User → Shipment (1:N)
Shipment → TrackingUpdate (1:N)
Shipment → Notification (1:N)
```

---

## 🚢 Deployment

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

### Docker
```bash
docker build -t fleeting-logistics .
docker run -p 8000:8000 fleeting-logistics
```

### DigitalOcean / AWS
See [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📈 Roadmap

### Phase 1 (May 2026)
- ✅ Design system & styling
- 🔄 Authentication
- 🔄 Basic dashboards

### Phase 2 (June 2026)
- Shipment tracking
- Admin features
- Mobile optimization

### Phase 3 (July 2026)
- API development
- Real-time notifications
- Analytics

### Phase 4 (August 2026)
- Performance optimization
- Security hardening
- Deployment setup

### Phase 5 (September 2026)
- Mobile app
- Advanced features
- Public launch

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 💬 Support

Need help? We're here!

- **Email**: support@fleetinglogistics.com
- **WhatsApp**: +256 752 276 350
- **Phone**: +256 752 276 350
- **Website**: https://www.fleetinglogistics.com

---

## 👥 Team

- **Founder & CEO**: [Your Name]
- **Lead Developer**: [Developer Name]
- **UI/UX Designer**: [Designer Name]
- **Project Manager**: [Manager Name]

---

## 📞 Contact

**Fleeting Logistics Company Limited**

- 📧 Email: info@fleetinglogistics.com
- 📱 WhatsApp: +256 752 276 350
- 📍 Location: Kampala, Uganda

---

## 🙏 Acknowledgments

- Django community
- Bootstrap team
- Font Awesome icons
- All contributors and supporters

---

**Made with ❤️ by the Fleeting Logistics Team**

---

### Quick Links
- [Upgrade Plan](UPGRADE_PLAN.md)
- [Implementation Guide](IMPLEMENTATION_GUIDE.md)
- [Project Board](https://github.com/yourusername/fleeting-logistics/projects)
- [Issue Tracker](https://github.com/yourusername/fleeting-logistics/issues)

