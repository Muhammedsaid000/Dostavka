# Generated by Django 5.1.4 on 2025-01-05 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_combo_description_en_combo_description_ku_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='combo',
            old_name='description_ku',
            new_name='description_ky',
        ),
        migrations.RenameField(
            model_name='combo',
            old_name='product_name_ku',
            new_name='product_name_ky',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='description_ku',
            new_name='description_ky',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_name_ku',
            new_name='product_name_ky',
        ),
    ]
