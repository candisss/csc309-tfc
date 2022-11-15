from django.urls import path

from subscriptions.views import CreateSubscriptionView, SubscriptionView, \
    SubscriptionsView

app_name = "Subscriptions"

urlpattern = [
    path('all/', SubscriptionsView.as_view()),
    path('new/', CreateSubscriptionView.as_view()),
    path('<int:subscription_id>/', SubscriptionView.as_view()),
]
