from datetime import date, timedelta as td

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Class, ClassOccurrence


@receiver(post_save, sender=Class, dispatch_uid="create_class_occurrences")
def create_class_occurrence(sender, instance, **kwargs):
    diff = ((instance.schedule_day - date.today().weekday()) + 7) % 7
    cur_date = date.today() + td(days=diff)
    while cur_date <= instance.end_recursion_date:
        ClassOccurrence.objects.get_or_create(class_obj=instance, date=cur_date)
        cur_date += td(days=7)
