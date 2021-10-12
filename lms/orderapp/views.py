from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from couponapp.models import Coupon
from courseapp.models import Course
from shortuuid import ShortUUID
from .models import *
import traceback

KEY="rzp_test_mUysLYnZLb381c"
SECRET_KEY="3zgKJ7VB1yym5UfAmz4k10dx"

import razorpay


# Create your views here.
class CreateOrderAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def createRazorPayOrder(self,user,amount):
        client = razorpay.Client(auth=(KEY, SECRET_KEY))
        data = { 
            "amount": int(amount*100), 
            "currency": "INR", 
            "receipt": f'splms-{ShortUUID().random(length=6).upper()}',
            "notes":{
                "id":user.id,
                "username":user.username
            },
            
            }
        order = client.order.create(data=data)
        return order

    def post(self,request):
        data=JSONParser().parse(request)
        serializer= OrderCreateSerializer(data=data)
        user=request.user

        if serializer.is_valid():
            data=serializer.validated_data
            course=data.get('course')
            body_courses=data.get('courses')
            coupon_code=data.get('coupon')
            courses=[]
            if course:
                courses=[course]
            if body_courses:
                courses=body_courses

            if coupon_code is not None:
                is_coupon_aplicable=True
                for course in courses:
                    is_valid = Coupon.is_valid(course,coupon_code)
                    is_coupon_aplicable = is_coupon_aplicable and is_valid
                if not is_coupon_aplicable:
                    return Response({
                        "coupon":["coupon is not valid for provided course or courses."]
                    },status=400)

            total_price=0
            after_discount_total_price=0
            for course in courses:
                total_price += course.price
                if not coupon_code:
                    sell_price= course.price - (course.price * course.discount * 0.01)
                else:
                    coupon=Coupon.objects.get(code=coupon_code,course=course)
                    coupon_discount=coupon.discount    
                    sell_price= course.price - (course.price * coupon_discount * 0.01)            
                after_discount_total_price += sell_price            

            rp_order=self.createRazorPayOrder(request.user,after_discount_total_price)
            order=Order(order_id= rp_order.get('id'),user=user)            
            order.save()

            for course in courses:
                order_item=OrderItem(course=course,order=order,price=course.price, discount=course.discount)
                if coupon_code is not None:
                    coupon=Coupon.objects.filter(code=coupon_code, course=course)[0]
                    order_item.coupon=coupon
                    order_item.discount=coupon.discount     
                order_item.save()

            orderSerializer=OrderSerializer(order)
            return Response(orderSerializer.data)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
           
class VerifyOrderApiView(APIView):
    def post(self, request):
        user=request.user
        data = JSONParser().parse(request)
        serializer=OrderVerifyDataSerializer(data=data)
        if serializer.is_valid():
            data=serializer.validated_data
            payment_id=data.get('razorpay_payment_id')
            order_id=data.get('razorpay_order_id')
            signature=data.get('razorpay_signature')
            
            try:
                order=Order.objects.get(order_id=order_id)
                if(order.order_status=="S"):
                    return Response({"order":"order already completed."},status=status.HTTP_400_BAD_REQUEST)
                client = razorpay.Client(auth=(KEY, SECRET_KEY))
                params_dict = {
                    'razorpay_order_id': order.order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature':signature
                }
                client.utility.verify_payment_signature(params_dict)
                order.order_status="S"
                order.payment_id=payment_id
                order.save()
                
            except:
                traceback.print_exc()
                return Response({"order":"order is not valid."},status=status.HTTP_400_BAD_REQUEST)

            return Response(OrderSerializer(order).data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
