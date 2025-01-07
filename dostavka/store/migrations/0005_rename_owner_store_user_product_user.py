# Generated by Django 5.1.4 on 2025-01-05 20:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_store_contact_info_alter_store_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='owner',
            new_name='user',
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
