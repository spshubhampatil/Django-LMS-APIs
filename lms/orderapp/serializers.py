from django.core.exceptions import ValidationError
from core.serializers import UserSerializer
from couponapp.serializers import CouponSerializer
from .models import *
from rest_framework.serializers import ModelSerializer,CharField,UUIDField
from rest_framework import serializers
from courseapp.models import Course
from rest_framework.response import Response
from rest_framework import status



def validateCouponCode(code):    
    count=Coupon.objects.filter(code=code).count()
    if count == 0:
        return ValidationError("coupon is not valid")

class OrderCreateSerializer(serializers.Serializer):
    courses=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(),many=True,required=False)
    course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(),required=False)
    coupon=serializers.CharField(required=False,validators=[validateCouponCode])

    def validate(self,attrs):
        error=ValidationError(
            {
                "course":"course or courses any one is required at a time..",
                "courses":"course or courses any one is required at a time.."
                }
            )
        data=dict(attrs)
        courses=data.get('courses')
        course=data.get('course')
        
        if (course and courses) or (not course and not courses):
            raise error

        return super().validate(attrs)
  

class OrderVerifyDataSerializer(serializers.Serializer):
    razorpay_payment_id= serializers.CharField()
    razorpay_order_id= serializers.CharField()
    razorpay_signature= serializers.CharField()


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    order_id=CharField(max_length=50,required=False)
    user=UserSerializer(read_only=True)
    coupon=CouponSerializer(read_only=True)
    order_items=OrderItemSerializer(read_only=True,many=True)

    class Meta:
        model = Order
        fields = '__all__'


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
