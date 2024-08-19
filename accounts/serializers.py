from rest_framework import serializers
from .models import Agency, Client, Consumer, Account


class ConsumerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Consumer model.

    This serializer handles the conversion of Consumer model instances
    to and from JSON format, including the 'name', 'address', and 'ssn' fields.
    """
    class Meta:
        model = Consumer
        fields = ['name', 'address', 'ssn']


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for the Account model.

    This serializer handles the conversion of Account model instances
    to and from JSON format, including the nested Consumer data.
    """
    consumer = ConsumerSerializer()

    class Meta:
        model = Account
        fields = ['client', 'consumer', 'balance', 'status']
