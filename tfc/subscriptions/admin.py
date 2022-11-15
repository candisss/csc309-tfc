from django.contrib import admin

from subscriptions.models import PaymentCard, PaymentHistory, Subscription

# Register your models here.

admin.site.register(Subscription)
admin.site.register(PaymentCard)
admin.site.register(PaymentHistory)
