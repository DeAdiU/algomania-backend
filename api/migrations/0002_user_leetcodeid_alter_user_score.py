# Generated by Django 5.0.7 on 2024-08-03 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='leetcodeId',
            field=models.CharField(max_length=128, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
