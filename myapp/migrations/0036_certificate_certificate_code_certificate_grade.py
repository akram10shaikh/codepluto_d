# Generated by Django 5.2 on 2025-05-29 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0035_alter_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='certificate_code',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='grade',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
