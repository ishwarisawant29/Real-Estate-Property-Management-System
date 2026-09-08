from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from django.utils import timezone


def create_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('properties', 'Profile')
    Property = apps.get_model('properties', 'Property')
    agent_ids = set(Property.objects.values_list('agent_id', flat=True))
    for user in User.objects.all():
        Profile.objects.get_or_create(
            user_id=user.id,
            defaults={'role': 'Agent' if user.id in agent_ids else 'Customer'}
        )


class Migration(migrations.Migration):
    dependencies = [
        ('properties', '0002_report_notification_created_at_review_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='reply',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Replied', 'Replied'), ('Closed', 'Closed')], default='Pending', max_length=20),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='replied_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(create_profiles, migrations.RunPython.noop),
    ]
