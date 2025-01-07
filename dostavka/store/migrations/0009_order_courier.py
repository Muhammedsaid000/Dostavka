# Generated by Django 5.1.4 on 2025-01-06 11:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_productsitem_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Ожидает обработки', 'Ожидает обработки'), ('В процессе доставки', 'В процессе доставки'), ('Доставлен', 'Доставлен'), ('Отменен', 'Отменен')], default='Ожидает обработки', max_length=32)),
                ('address', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productsitem')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL)),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courier_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('занят', 'занят'), ('доступен', 'доступен')], max_length=32)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courier', to=settings.AUTH_USER_MODEL)),
                ('current_orders', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='store.order')),
            ],
        ),
    ]
