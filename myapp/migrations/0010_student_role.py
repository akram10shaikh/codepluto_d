# Generated by Django 5.1.1 on 2025-03-10 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_customuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='role',
            field=models.CharField(choices=[('software developer', 'Software Developer'), ('backend developer', 'Backend Developer'), ('frontend developer', 'Frontend Developer')], default='software developer', max_length=30, null=True),
        ),
    ]
