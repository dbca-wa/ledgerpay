from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from ledgerpay.models import PaymentItem
from ledgerpay.serializers import PaymentItemSerializer


class PaymentItemViewSet(viewsets.ModelViewSet):
    queryset = PaymentItem.objects.all()

    @list_route(methods=['GET',])
    def list_for_external(self, request, *args, **kwargs):
        payment_item_qs = self.get_queryset().filter(enabled=True)
        serializer = PaymentItemSerializer(payment_item_qs, many=True)
        return Response(serializer.data)
