# Generated by Django 5.2 on 2025-06-13 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0052_bookclass_completed_meeting_completed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_Demo_Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('phone_number', models.IntegerField(null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M', max_length=10)),
                ('amount', models.IntegerField(null=True)),
                ('invoice', models.CharField(max_length=100, null=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.teacher')),
            ],
        ),
    ]
