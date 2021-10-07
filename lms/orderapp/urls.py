from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
   path('create/',CreateOrderAPIView.as_view(),name='create-order'),
   path('verify/',VerifyOrderApiView.as_view(),name='order-verify')
]
