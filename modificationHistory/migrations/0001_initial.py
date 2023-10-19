# Generated by Django 4.2.6 on 2023-10-19 01:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appEstablishment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appFieldSoccer', '0001_initial'),
        ('appReservation', '0001_initial'),
        ('appUser', '0001_initial'),
        ('typeThings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=150)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('created_user', models.IntegerField(null=True)),
                ('updated_user', models.IntegerField(null=True)),
                ('deleted_user', models.IntegerField(null=True)),
                ('rol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_rol', to='appUser.rol')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_id_history_users', to=settings.AUTH_USER_MODEL)),
                ('user_session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_session_history_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'history_users',
            },
        ),
        migrations.CreateModel(
            name='HistoryReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_hour', models.DateTimeField()),
                ('end_hour', models.DateTimeField()),
                ('status', models.BooleanField(verbose_name=False)),
                ('created_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('created_user', models.IntegerField(null=True)),
                ('updated_user', models.IntegerField(null=True)),
                ('deleted_user', models.IntegerField(null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_reservation_customer', to=settings.AUTH_USER_MODEL)),
                ('field_soccer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_reservation_field_soccer', to='appFieldSoccer.fieldsoccer')),
                ('reservation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation_id_history_users', to='appReservation.reservation')),
                ('user_session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_session_history_reservation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'history_reservation',
            },
        ),
        migrations.CreateModel(
            name='HistoryFieldSoccer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('number_players', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('status', models.BooleanField(verbose_name=False)),
                ('created_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('created_user', models.IntegerField(null=True)),
                ('updated_user', models.IntegerField(null=True)),
                ('deleted_user', models.IntegerField(null=True)),
                ('establishment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_type_field_soccer_establishment', to='appEstablishment.establishment')),
                ('field_soccer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_soccer_id_history_users', to='appFieldSoccer.fieldsoccer')),
                ('type_field_soccer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_type_field_soccer', to='typeThings.typefieldsoccer')),
                ('user_session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_session_history_field_soccers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'history_field_soccers',
            },
        ),
        migrations.CreateModel(
            name='HistoryEstablishment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('location', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=20)),
                ('status', models.BooleanField(verbose_name=False)),
                ('created_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('created_user', models.IntegerField(null=True)),
                ('updated_user', models.IntegerField(null=True)),
                ('deleted_user', models.IntegerField(null=True)),
                ('establishment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='establishment_id_history_users', to='appEstablishment.establishment')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_establishment_owner', to=settings.AUTH_USER_MODEL)),
                ('type_dep', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_establishment_type_dep', to='typeThings.typedepartament')),
                ('type_dist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_establishment_type_dist', to='typeThings.typedistrict')),
                ('type_prov', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_establishment_type_prov', to='typeThings.typeprovince')),
                ('user_session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_session_history_establishments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'history_establishments',
            },
        ),
    ]
