from django.contrib import admin

# Register your models here.
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')

    fieldsets = (
        ('Basic', {'fields': ('first_name', 'last_name', 'username', 'email', 'phone_num', 'avatar', 'subscription', 'is_admin', 'is_staff',
                             'is_superuser')}),
    )
