from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import *
from rest_framework.routers import DefaultRouter


coupon_router=DefaultRouter()
coupon_router.register("",CouponModelViewSet,basename='coupon')

urlpatterns = [
   path('course/<str:course_id>/code/<str:code>',CouponRetrieveViewByCode.as_view(),name='coupon-bycode'),
   path('',include(coupon_router.urls))
]