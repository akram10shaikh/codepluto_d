# Generated by Django 5.2 on 2025-06-13 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0056_remove_badge_badge_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='badge_level',
            field=models.CharField(choices=[('Rising Star', 'Rising Star'), ('Certified Mentor', 'Certified Mentor'), ('Elite Educato', 'Elite Educato'), ('Master Coach', 'Master Coach')], default='Rising Star', max_length=100),
        ),
    ]
