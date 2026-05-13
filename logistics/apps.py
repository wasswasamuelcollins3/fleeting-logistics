import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


def _ensure_site_for_site_id(sender, app_config, **kwargs):
    """django.contrib.sites: allauth calls get_current_site(); missing Site row → 500."""
    if app_config.label not in ("sites", "logistics"):
        return
    try:
        from django.apps import apps as django_apps
        from django.conf import settings
        from django.contrib.sites.models import Site
        from django.db.utils import OperationalError, ProgrammingError

        if not django_apps.is_installed("django.contrib.sites"):
            return
        sid = getattr(settings, "SITE_ID", None)
        if not sid:
            return
        if Site.objects.filter(pk=sid).exists():
            return
        domain = (getattr(settings, "DEFAULT_SITE_DOMAIN", None) or "example.com")[:100]
        name = domain[:50]
        Site.objects.create(pk=sid, domain=domain, name=name)
        logger.warning(
            "Created django.contrib.sites.Site pk=%s domain=%s "
            "(set DEFAULT_SITE_DOMAIN on your host, e.g. your-app.onrender.com).",
            sid,
            domain,
        )
    except (ProgrammingError, OperationalError):
        return
    except Exception:
        logger.exception("Could not ensure django.contrib.sites.Site exists")


class LogisticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "logistics"

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(_ensure_site_for_site_id)
