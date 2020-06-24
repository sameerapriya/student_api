from django.db import models
from django.contrib.auth.models import AbstractUser


class Student(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True)
    student_count = models.IntegerField(default=0)
    max_student_count = models.IntegerField(default=5)

    def __str__(self):
        return self.name


class CourseEnroll(models.Model):
    student = models.ForeignKey('Student', on_delete=models.PROTECT)
    course = models.ForeignKey('Course', on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student}:{self.course}'
