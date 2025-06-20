# Generated by Django 5.2 on 2025-04-30 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0032_enrollment_total_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollment',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='enrollment',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='enrollment',
            name='total_days',
        ),
        migrations.AddField(
            model_name='enrollment',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='google_event_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='meet_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='recording_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.teacher'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.teacher'),
        ),
    ]
