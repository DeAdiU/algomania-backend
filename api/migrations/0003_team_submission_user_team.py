# Generated by Django 5.0.7 on 2024-08-04 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_leetcodeid_alter_user_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.AutoField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=255)),
                ('Score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('submission_id', models.IntegerField(unique=True)),
                ('category', models.CharField(choices=[('PROF', 'Professor'), ('NML', 'Normal'), ('BIWL', 'Biweekly'), ('WL', 'Weekly'), ('POTD', 'Problem of the day')], max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('titleSlug', models.SlugField(max_length=255, unique=True)),
                ('difficulty', models.CharField(choices=[('Easy', 'EASY'), ('Medium', 'MEDIUM'), ('Hard', 'HARD')], max_length=10)),
                ('points', models.IntegerField()),
                ('submission_time', models.DateTimeField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='api.user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='api.team'),
        ),
    ]