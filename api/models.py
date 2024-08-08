from django.db import models
from django.utils.text import slugify
from enum import Enum
# Create your models here.



class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class Category(models.TextChoices):
    PROFESSOR = 'PROF', 'Professor'
    NORMAL = 'NML', 'Normal'
    CONTEST = 'CONT', 'Contest'
    POTD = 'POTD', 'Problem of the day'


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=255)

    def __str__(self):
        return self.team_name

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    score = models.IntegerField(default=0,null=True,blank=True)
    leetcodeId = models.CharField(max_length=128, unique=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members', null=True, blank=True)

    def __str__(self):
        return f"Submission {self.email} by {self.leetcodeId}"
    


class Submission(models.Model):
    question_id = models.AutoField(primary_key=True)
    leetcodeQuestionId = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    submission_id = models.IntegerField(unique=True)
    category = models.CharField(max_length=10, choices=Category.choices)
    title = models.CharField(max_length=255)
    titleSlug = models.SlugField(max_length=255, unique=True)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices())
    points = models.IntegerField()
    submission_time = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.question_id} by {self.user} and {self.leetcodeQuestionId}"


class TeacherQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField()
    title = models.CharField(max_length=255)
    url = models.URLField()
    titleSlug = models.SlugField(max_length=255, unique=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return f"TeacherQuestion {self.id} with {self.questions.count()} questions"