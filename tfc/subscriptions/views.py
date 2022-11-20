from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, RetrieveAPIView, \
    ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from subscriptions.models import PaymentHistory, Subscription
from subscriptions.serializers import PaymentCardSerializer, \
    PaymentHistorySerializer, \
    SubscriptionSerializer


# Create your views here.
class SubscriptionView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SubscriptionSerializer

    def get_object(self):
        return get_object_or_404(Subscription,
                                 id=self.kwargs['subscription_id'])


class SubscriptionsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.all()


class CreateSubscriptionView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SubscriptionSerializer


class PaymentHistoryView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentHistorySerializer

    def get_object(self):
        return self.request.user.payment_histories


class PaymentCardView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentCardSerializer

    def get_object(self):
        return self.request.user.payment_cards


# class EditSubscriptionView(UpdateAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = SubscriptionSerializer
#
#     def get_object(self):
#         return get_object_or_404(Subscription,
#                                  id=self.kwargs['subscription_id'])
#
#
# class DeleteSubscriptionView(DestroyAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = SubscriptionSerializer
#
#     def get_object(self):
#         return get_object_or_404(Subscription,
#                                  id=self.kwargs['subscription_id'])
