from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    score = models.IntegerField(default=0,null=True,blank=True)
    leetcodeId = models.CharField(max_length=128, unique=True, null=True)

    def __str__(self):
        return self.email
    

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=255)
    Score = models.IntegerField()

    def __str__(self):
        return self.team_name

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    member_name = models.CharField(max_length=255)
    score = models.IntegerField()
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.member_name

class Submission(models.Model):
    question_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='questions')
    easy = models.IntegerField()
    medium = models.IntegerField()
    hard = models.IntegerField()
    potd = models.IntegerField()

    def __str__(self):
        return f"Question {self.question_id} by {self.member}"
