# api/serializers.py

from rest_framework import serializers
from .models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = UserAccount
        fields = ('uid', 'first_name', 'last_name', 'email', 'billing_address', 
        'shipping_address' , 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')