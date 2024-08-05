from django.contrib import admin
from .models import TeacherQuestion,User,Submission
# Register your models here.

admin.site.register(TeacherQuestion)
admin.site.register(User)
admin.site.register(Submission)
