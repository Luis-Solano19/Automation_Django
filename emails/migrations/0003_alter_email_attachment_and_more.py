# Generated by Django 5.0.6 on 2024-06-25 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_email_subscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='attachment',
            field=models.FileField(blank=True, upload_to='email_attachments/'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='email_address',
            field=models.EmailField(max_length=100),
        ),
    ]
