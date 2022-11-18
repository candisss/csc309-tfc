from django.contrib import admin
from datetime import date, timedelta as td

from classes.models import Class, Keyword, ClassOccurrence


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'capacity', 'schedule_day', 'start_time', 'end_time')

    actions = ['create_class_occurrences']

    def create_class_occurrences(self, request, queryset):
        for class_obj in queryset:
            diff = ((class_obj.schedule_day - date.today().weekday()) + 7) % 7
            cur_date = date.today() + td(days=diff)
            while cur_date <= class_obj.end_recursion_date:
                ClassOccurrence.objects.get_or_create(class_obj=class_obj, date=cur_date)
                cur_date += td(days=7)

        self.message_user(request, f'Class occurrence created for {len(queryset)} classes.')


@admin.register(ClassOccurrence)
class ClassOccurrenceAdmin(admin.ModelAdmin):
    list_display = ('class_obj', 'date', 'cancelled')
    ordering = ('date',)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name',)
