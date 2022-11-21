from django.urls import path

from subscriptions.views import CancelSubscriptionView, CheckSubscriptionView, \
    CreatePaymentCardView, CreateSubscriptionView, \
    ManageView, PaymentCardView, \
    PaymentHistoryView, \
    SubscribeView, SubscriptionView, \
    SubscriptionsView

app_name = "Subscriptions"

urlpatterns = [
    path('all/', SubscriptionsView.as_view(), name="subscriptions"),
    path('new/', CreateSubscriptionView.as_view(), name="new-subscription"),
    path('<int:subscription_id>/', SubscriptionView.as_view(), name="subscription"),
    path('subscribe/', SubscribeView().as_view(), name="subscribe"),
    path('check-subscription/', CheckSubscriptionView.as_view(), name="check_subscription"),
    path('cancel-subscription/', CancelSubscriptionView.as_view(), name="cancel_subscription"),
    path('manage/', ManageView.as_view(), name="manage"),
    path('history/', PaymentHistoryView.as_view(), name="payment_history"),
    path('payment-card/', PaymentCardView.as_view(), name="payment_card"),
    path('new-payment-card/', CreatePaymentCardView.as_view(), name="create_payment_card")
]
