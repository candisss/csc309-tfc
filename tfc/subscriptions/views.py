from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, GenericAPIView, \
    RetrieveAPIView, \
    ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer

from subscriptions.models import PaymentCard

from subscriptions.serializers import PaymentCardsSerializer


# Create your views here.
# class SubscriptionView(RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = SubscriptionSerializer
#
#     def get_object(self):
#         return get_object_or_404(Subscription,
#                                  id=self.kwargs['subscription_id'])


# class SubscriptionsView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = SubscriptionSerializer
#
#     def get_queryset(self):
#         return Subscription.objects.all()


# class CreateSubscriptionView(CreateAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = SubscriptionSerializer


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

# class SubscribeView()

class AddPaymentView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentCardsSerializer
    #
    # def get_serializer_context(self):
    #     """
    #     Extra context provided to the serializer class.
    #     """
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }
    def post(self, request):
        serializer = PaymentCardsSerializer(data=request.data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        # serializer.user = user
        serializer.save()
        return Response(serializer.data)

