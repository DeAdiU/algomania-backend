from django.contrib import admin
from .models import TeacherQuestion,User,Submission,Team
# Register your models here.

admin.site.register(TeacherQuestion)
admin.site.register(User)
admin.site.register(Submission)
admin.site.register(Team)
