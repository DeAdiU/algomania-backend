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