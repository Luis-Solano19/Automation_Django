# Generated by Django 5.0.6 on 2024-06-26 02:27

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0005_alter_email_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
