# Generated by Django 5.2 on 2025-05-30 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0042_alter_certificate_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='completion_date',
            field=models.DateTimeField(null=True),
        ),
    ]
