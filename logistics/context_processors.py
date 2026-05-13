"""Template context shared across the site."""
from urllib.parse import quote

from django.conf import settings


def company_contact(_request):
    digits = getattr(settings, "WHATSAPP_PHONE_DIGITS", "256768383164")
    default_msg = "Hello Fleeting Logistics, I would like to book a service."
    return {
        "WHATSAPP_PHONE_DIGITS": digits,
        "WHATSAPP_WA_URL": f"https://wa.me/{digits}",
        "WHATSAPP_FLOAT_URL": f"https://wa.me/{digits}?text={quote(default_msg)}",
        "SUPPORT_PHONE_DISPLAY": getattr(settings, "SUPPORT_PHONE_DISPLAY", "+256 768 383 164"),
        "SUPPORT_PHONE_E164": getattr(settings, "SUPPORT_PHONE_E164", "+256768383164"),
    }
