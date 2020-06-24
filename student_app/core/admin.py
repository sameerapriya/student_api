from django.contrib import admin
from core import models


admin.site.register(models.Student)
admin.site.register(models.Course)
admin.site.register(models.CourseEnroll)
