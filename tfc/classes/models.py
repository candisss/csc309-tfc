from django.db import models

from accounts.models import CustomUser
from studios.models import Studio


class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Keywords'


class Class(models.Model):
    name = models.CharField(max_length=125)
    description = models.TextField(blank=True, null=True)
    coach = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='class_coach')
    keywords = models.ManyToManyField(Keyword, blank=True)
    capacity = models.IntegerField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    cancelled = models.BooleanField(default=False)

    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='class_studio')

    students_enrolled = models.ManyToManyField(CustomUser, blank=True, related_name='class_studentsenrolled')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
