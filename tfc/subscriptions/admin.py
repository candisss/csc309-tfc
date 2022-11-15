from django.contrib import admin

from subscriptions.models import PaymentCards, PaymentHistory, Subscriptions

# Register your models here.

admin.site.register(Subscriptions)
admin.site.register(PaymentCards)
admin.site.register(PaymentHistory)
