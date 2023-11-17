# Generated by Django 4.2.6 on 2023-11-16 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeThings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('status', models.BooleanField(verbose_name=False)),
            ],
            options={
                'db_table': 'type_status',
            },
        ),
    ]
