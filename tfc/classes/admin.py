from datetime import date, timedelta as td

from django.contrib import admin

from classes.models import Class, Keyword, ClassOccurrence


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'capacity', 'schedule_day', 'start_time', 'end_time')

    actions = ['cancel_all_occurrences']



    def cancel_all_occurrences(self, request, queryset):
        for class_obj in queryset:
            class_obj.class_occurrence_class_obj.exclude(cancelled=True).filter(date__gte=date.today()).update(
                cancelled=True)

        self.message_user(request, f'All the future instances the selected classes have been cancelled.')




@admin.register(ClassOccurrence)
class ClassOccurrenceAdmin(admin.ModelAdmin):
    list_display = ('class_obj', 'date', 'cancelled')
    ordering = ('date',)

    actions = ['cancel_all_occurrences']

    def cancel_all_occurrences(self, request, queryset):
        queryset.exclude(cancelled=True).filter(date__gte=date.today()).update(cancelled=True)
        self.message_user(request, f'All the selected future instances have been cancelled.')


        self.message_user(request, f'Class occurrence created for {len(queryset)} classes.')


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name',)
