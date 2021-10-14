from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['first_name','last_name','email','username','is_superuser']

    # def to_representation(self, instance):        
    #     json= super().to_representation(instance)
    #     json.pop('password')
    #     return json