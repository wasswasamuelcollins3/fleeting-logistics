from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0002_service_remove_booking_service_type_booking_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_type',
            field=models.CharField(choices=[('cargo', 'Cargo Transport'), ('passenger', 'Passenger Transport'), ('express', 'Express Delivery'), ('warehousing', 'Warehousing'), ('customs', 'Customs Clearance')], default='cargo', max_length=20),
        ),
        migrations.AddField(
            model_name='service',
            name='price_per_kg',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='service',
            name='estimated_delivery_days',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='service',
            name='icon',
            field=models.CharField(blank=True, help_text='FontAwesome icon class', max_length=50),
        ),
        migrations.AddField(
            model_name='service',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
