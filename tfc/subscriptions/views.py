import datetime
from dateutil import relativedelta

from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, GenericAPIView, \
    RetrieveAPIView, \
    ListAPIView, CreateAPIView, \
    RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
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
    pagination_class = PageNumberPagination


    def get_object(self):
        return get_object_or_404(Subscription,
                                 id=self.kwargs['subscription_id'])


class SubscriptionsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SubscriptionSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Subscription.objects.all()


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            print(Subscription.objects.get(id=request.data.get('subscription_id')))
            Subscription.objects.get(id=request.data.get('subscription_id'))
        except Exception:
            return Response("No Subscription Found", status=404)
        try:
            self.request.user.payment_card
        except Exception:
            return Response("No Payment Card Found", status=404)
        subscription = Subscription.objects.get(
            id=request.data.get('subscription_id'))
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
    pagination_class = PageNumberPagination


    def get_object(self):
        try:
            self.request.user.subscription
        except Exception:
            return Response("User not subscribed", status=404)
        return self.request.user.subscription


class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # cancel classes after user.next_payment_date

        # remove sub from user
        user = request.user
        user.subscription = None
        user.subscribed = False
        user.next_payment_date = None
        user.save()
        return Response("Subscription Cancelled Successfully", status=200)


class CreateSubscriptionView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SubscriptionSerializer


class PaymentHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentHistorySerializer
    pagination_class = PageNumberPagination


    def get_queryset(self):
        return self.request.user.payment_histories.all()


class PaymentCardView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentCardSerializer
    pagination_class = PageNumberPagination

    def get_object(self):
        try:
            self.request.user.payment_card
        except Exception:
            return Response("No card found", status=404)
        return self.request.user.payment_card


class CreatePaymentCardView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentCardSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ManageView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        users = CustomUser.objects.all()
        for user in users:
            if user.subscribed and user.next_payment_date.date() == datetime.today().date():
                result = charge(user.payment_card)
                if result:
                    generate_history(user.subscription.price, user.payment_card,
                                     user)
                    update_next_payment_time(user)
                else:
                    user.subscription = None
                    user.subscribed = False
                    user.next_payment_date = None
                    user.save()
        return Response("Managed Successfully", status=200)


class NextPaymentDateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get(self, request):
        user = request.user
        return Response(user.next_payment_date.__str__(), status=200)

def charge(payment_card):
    # a fake charge card func that always returns true
    return True


def generate_history(amount, card, user):
    payment_history = PaymentHistory(amount_paid=amount, payment_card=card,
                                     user=user)
    payment_history.save()


def update_next_payment_time(user):
    if user.next_payment_date is None:
        date = datetime.date.today()
    else:
        date = user.next_payment_date
    if user.subscription.term == "YEAR":
        user.next_payment_date = date + relativedelta.relativedelta(
            months=1)
        user.save()
    elif user.subscription.term == "MONTH":
        user.next_payment_date = date + relativedelta.relativedelta(
            years=1)
        user.save()
    else:
        raise AttributeError("No Subscription Term Found")
