from django.db import models
from django.db.models import Max

from accounts.models import CustomUser
from studios.models import Studio


class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Keywords'


class Class(models.Model):
    SCHEDULE_DAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Tuesday'),
    )
    name = models.CharField(max_length=125)
    description = models.TextField(blank=True, null=True)
    coach = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='class_coach')
    keywords = models.ManyToManyField(Keyword, blank=True)
    capacity = models.IntegerField()
    schedule_day = models.IntegerField(choices=SCHEDULE_DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    end_recursion_date = models.DateField()
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='class_studio')

    def is_full(self):
        max_students = self.class_occurrence_class_obj.aggregate(max=Max('students_enrolled')).get('max')
        if max_students == self.capacity:
            return True
        else:
            return False

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'


class ClassOccurrence(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Class', related_name='class_occurrence_class_obj')
    date = models.DateField(null=True)
    students_enrolled = models.ManyToManyField(CustomUser, blank=True, related_name='class_occurrence_students_enrolled')
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.class_obj.name} occurrence'

    class Meta:
        verbose_name = 'Class Occurrence'
        verbose_name_plural = 'Classes Occurrences'
