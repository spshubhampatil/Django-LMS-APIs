from django.contrib import admin
from django.urls import path
from rest_framework import urlpatterns
from .views import *
from rest_framework.routers import DefaultRouter



doubt_router=DefaultRouter()
doubt_router.register("answer",DoubtAnswerModelViewSet, basename='doubt-answer')
doubt_router.register("",DoubtModelViewSet, basename='doubt')


urlpatterns=[]
urlpatterns += doubt_router.urls
