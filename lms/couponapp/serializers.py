from .models import *
from rest_framework.serializers import ModelSerializer

class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

