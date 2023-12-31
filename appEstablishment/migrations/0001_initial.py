# Generated by Django 4.2.6 on 2023-12-11 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('typeThings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Establishment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('location', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=20)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('status', models.BooleanField(verbose_name=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('created_user', models.IntegerField(null=True)),
                ('updated_user', models.IntegerField(null=True)),
                ('deleted_user', models.IntegerField(null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='establishment_owner', to=settings.AUTH_USER_MODEL)),
                ('type_dep', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='establishment_type_dep', to='typeThings.typedepartament')),
                ('type_dist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='establishment_type_dist', to='typeThings.typedistrict')),
                ('type_prov', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='establishment_type_prov', to='typeThings.typeprovince')),
            ],
            options={
                'db_table': 'establishments',
            },
        ),
    ]
