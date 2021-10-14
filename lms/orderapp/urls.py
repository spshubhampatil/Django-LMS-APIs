from django.contrib import admin
from django.urls import path

from .views import *

Orderurls = [
   path('create/',CreateOrderAPIView.as_view(),name='create-order'),
   path('verify/',VerifyOrderApiView.as_view(),name='order-verify')
]


Subscriptionurls = [
   path('',SubscriptionListView.as_view(),name='subscription-list'),
   path('user/<int:pk>',CourseSubscribedByUser.as_view(),name='subscription-list-of-user'),   
]
