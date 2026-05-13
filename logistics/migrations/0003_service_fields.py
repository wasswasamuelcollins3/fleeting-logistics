from django.db import migrations


class Migration(migrations.Migration):
    """
    Service columns were already created on Service in 0002.
    This migration is kept as a no-op so the dependency chain stays valid.
    """

    dependencies = [
        ("logistics", "0002_service_remove_booking_service_type_booking_status_and_more"),
    ]

    operations = []
