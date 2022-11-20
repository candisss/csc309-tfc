from datetime import datetime
from dateutil import relativedelta

from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, RetrieveAPIView, \
    ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser
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
    permission_classes = [AllowAny]
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.all()


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self):
        if not Subscription.objects.filter(id=self.kwargs['subscription_id']).exists():
            return Response("No Subscription Found", status=404)
        if not self.request.user.payment_card.exists():
            return Response("No Payment Card Found", status=404)
        subscription = Subscription.objects.filter(id=self.kwargs['subscription_id'])
        user = self.request.user
        if charge(user.payment_card):
            user.subscription = subscription
            user.subscribed = True
            charge(user.payment_card)
            generate_history(subscription.price, user.payment_card, user)
            update_next_payment_time(user)
            user.save()
        else:
            return Response("Charge Failed", status=400)
        return Response("Subscribed Successfully", status=200)


class CheckSubscriptionView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_object(self):
        return self.request.user.subscription


class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self):
        user = self.request.user
        user.subscription = None
        user.subscribed = False
        user.next_payment_date = None
        user.save()
        return Response("Subscription Cancelled Successfully", status=200)


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
        return self.request.user.payment_card


class ManageView(APIView):
    permission_classes = [IsAdminUser]

    def post(self):
        users = CustomUser.objects.all()
        for user in users:
            if user.subscribed and user.next_payment_date.date() == datetime.today().date():
                charge(user.payment_card)
                generate_history(user.subscription.price, user.payment_card, user)
                update_next_payment_time(user)
        return Response("Subscription Cancelled Successfully", status=200)


def charge(payment_card):
    # a fake charge card func that always returns true
    return True


def generate_history(amount, card, user):
    payment_history = PaymentHistory(amount_paid=amount, payment_card=card, user=user)
    payment_history.save()


def update_next_payment_time(user):
    if user.subscription.term == "Year":
        user.next_payment_date = datetime.date.today() + relativedelta.relativedelta(
            months=1)
        user.save()
    elif user.subscription.term == "Month":
        user.next_payment_date = datetime.date.today() + relativedelta.relativedelta(
            years=1)
        user.save()
    else:
        raise AttributeError()
