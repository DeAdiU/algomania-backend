# Generated by Django 5.0.7 on 2024-08-07 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_submission_leetcodequestionid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='Score',
        ),
    ]