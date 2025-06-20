# Generated by Django 5.2 on 2025-04-15 08:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_remove_student_classes_live_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(upload_to='pdf_file/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.courses')),
            ],
        ),
    ]
