# Generated by Django 5.1.4 on 2025-02-14 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urban', '0006_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic'),
        ),
    ]
