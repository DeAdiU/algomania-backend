# Generated by Django 5.0.7 on 2024-08-05 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_submission_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='leetcodeQuestionId',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
