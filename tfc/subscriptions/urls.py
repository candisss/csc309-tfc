from django.urls import path

from subscriptions.views import AddPaymentView

# from subscriptions.views import CreateSubscriptionView, SubscriptionView, \
#     SubscriptionsView

app_name = "Subscriptions"

urlpatterns = [
    # path('all/', SubscriptionsView.as_view()),
    # path('new/', CreateSubscriptionView.as_view()),
    # path('<int:subscription_id>/', SubscriptionView.as_view()),
    path('cards/add', AddPaymentView.as_view(), name='add_payment'),
]
