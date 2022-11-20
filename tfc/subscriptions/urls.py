from django.urls import path

from subscriptions.views import CreateSubscriptionView, PaymentCardView, \
    PaymentHistoryView, \
    SubscriptionView, \
    SubscriptionsView

app_name = "Subscriptions"

urlpatterns = [
    path('all/', SubscriptionsView.as_view(), name="subscriptions"),
    path('new/', CreateSubscriptionView.as_view(), name="new-subscription"),
    path('<int:subscription_id>/', SubscriptionView.as_view(), name="subscription"),
    path('history/', PaymentHistoryView.as_view(), name="payment_history"),
    path('payment-card/', PaymentCardView.as_view(), name="payment_card"),
]
