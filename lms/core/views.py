from django.http import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def api_root(request):
    response={
        "API ROOT": reverse('api_root', request=request),

        "Auth Token":{
            "Access Token":reverse('token_obtain_pair',request=request),
            "Token Refresh":reverse('token_refresh',request=request),
            "Token Verify":reverse('token_verify',request=request)
        },

        "Course":{
            "Course List": reverse('courses:course-list', request=request),
            "Course Detail": reverse('courses:course-detail',args=[1], request=request),
            "Course Detail by Slug": reverse('courses:course-detail-by-slug',args=['course-slug'], request=request),
            "Courses by Category": reverse('courses:courses-by-category',args=['category-id'], request=request),
        },

        "Tag":{
            "Tag List": reverse('courses:tag-list', request=request),
            "Tag Detail": reverse('courses:tag-detail',args=['tag-id'], request=request),
            
        },

        "Category":{
            "Category List": reverse('courses:category-list', request=request),
            "Category Detail": reverse('courses:category-detail',args=['category-id'], request=request),
            "Category Detail by Slug": reverse('courses:category-detail-by-slug',args=['category-slug'], request=request),
        },
        "Chapter":{
            "Chapter Types":reverse('chapters:chapter-type-view',request=request),            
            "Chapter Create":reverse('chapters:chapter-createview',request=request),
            "Chapter By Course":reverse('chapters:chapter-listview',args=['course-id'],request=request),
            "Video Platform List":reverse('chapters:video-platform-listview',request=request),
        },
        "Coupon":{
            "Coupon List":reverse('coupons:coupon-list',request=request),            
            "Coupon Detail":reverse('coupons:coupon-detail',args=['coupon-id'],request=request),
            "Coupon By Code":reverse('coupons:coupon-bycode',args=['course-id','coupon-code'],request=request),
            
        } ,
        "Order":{
            "Create Order":reverse('orders:create-order',request=request),
            "Verify Order":reverse('orders:order-verify',request=request),
        },
        "Subscription":{
            "Subscription List":reverse('subscriptions:subscription-list',request=request),
           
        },
        "Review":{
            "Review List":reverse('reviews:reviews-list',request=request),
            "Review Detail":reverse('reviews:reviews-detail',args=['review-id'],request=request),           
        },
        "Doubt":{
            "Doubts List":reverse('doubts:doubt-list',request=request),
            "Doubts Detail":reverse('doubts:doubt-detail',args=['doubt-id'],request=request),           
        }
    }
    return Response(response)