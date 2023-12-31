# Generated by Django 4.2.6 on 2023-12-11 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appFieldSoccer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('typeThings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_hour', models.TimeField()),
                ('end_hour', models.TimeField()),
                ('reminder_sent', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('created_user', models.IntegerField(null=True)),
                ('updated_user', models.IntegerField(null=True)),
                ('deleted_user', models.IntegerField(null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation_customer', to=settings.AUTH_USER_MODEL)),
                ('field_soccer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation_field_soccer', to='appFieldSoccer.fieldsoccer')),
                ('type_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation_type_status', to='typeThings.typestatus')),
            ],
            options={
                'db_table': 'reservation',
            },
        ),
    ]
