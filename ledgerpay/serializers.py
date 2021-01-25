from rest_framework import serializers

from ledgerpay.models import PaymentItem


class PaymentItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentItem
        fields = (
            'id',
            'display_name',
            'api_url',
            'description',
        )
