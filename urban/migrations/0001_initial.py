# Generated by Django 5.0 on 2025-02-12 03:26

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='ads/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the person giving feedback', max_length=255)),
                ('message', models.TextField(help_text='The feedback message')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when feedback was created')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_pic', models.ImageField(blank=True, null=True, upload_to='service_pic')),
                ('skills', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=25)),
                ('service_rate', models.CharField(max_length=25)),
                ('phone', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(default='address', max_length=50)),
                ('pincode', models.CharField(default='pincode', max_length=6)),
                ('city', models.CharField(max_length=25)),
                ('district', models.CharField(default='district', max_length=25)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic')),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('lat', models.FloatField(default=0, null=True)),
                ('long', models.FloatField(default=0, null=True)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Order Confirmed', 'Order Confirmed'), ('Delivered', 'Delivered')], max_length=50, null=True)),
                ('consumer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='urban.consumer')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='urban.services')),
            ],
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('professional_details', models.CharField(max_length=250)),
                ('contractor_id_proof', models.FileField(max_length=20, upload_to='')),
                ('address', models.CharField(default='address', max_length=50)),
                ('pincode', models.CharField(default='pincode', max_length=6)),
                ('city', models.CharField(max_length=25)),
                ('district', models.CharField(default='district', max_length=25)),
                ('status', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Adpayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='urban.contractor')),
            ],
        ),
        migrations.CreateModel(
            name='CServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_pic', models.ImageField(blank=True, null=True, upload_to='service_pic')),
                ('skills', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=25)),
                ('service_rate', models.CharField(max_length=25)),
                ('phone', models.PositiveBigIntegerField()),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urban.contractor')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker', models.CharField(default='hai', max_length=16)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('card_number', models.CharField(max_length=16)),
                ('account_holder_name', models.CharField(max_length=100)),
                ('cvv', models.CharField(max_length=3)),
                ('expiry_date', models.DateField()),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urban.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('skills', models.CharField(max_length=30)),
                ('work_experience', models.CharField(max_length=20)),
                ('address', models.CharField(default='address', max_length=50)),
                ('pincode', models.CharField(default='pincode', max_length=6)),
                ('city', models.CharField(max_length=25)),
                ('district', models.CharField(default='district', max_length=25)),
                ('aadhar_number', models.CharField(default='Pending', max_length=12)),
                ('service_rate', models.CharField(max_length=30)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('profile_pic', models.FileField(blank=True, default='profile_files/default.pdf', null=True, upload_to='profile_files')),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='services',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urban.worker'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='workers',
            field=models.ManyToManyField(blank=True, to='urban.worker'),
        ),
        migrations.AddField(
            model_name='consumer',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='urban.worker'),
        ),
        migrations.CreateModel(
            name='Chatmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('consumer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='urban.consumer')),
                ('worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='urban.worker')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='urban.worker'),
        ),
        migrations.CreateModel(
            name='Workerabout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('workimage1', models.ImageField(blank=True, null=True, upload_to='')),
                ('workimage2', models.ImageField(blank=True, null=True, upload_to='')),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='urban.worker')),
            ],
        ),
    ]
