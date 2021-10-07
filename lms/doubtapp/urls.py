from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path('',testview,name='test-api')
]