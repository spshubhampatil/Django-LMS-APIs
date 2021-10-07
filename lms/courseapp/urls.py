from django.contrib import admin
from django.db.models import base
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

category_router=DefaultRouter()
category_router.register('',CategoryViewSet,basename='category')

course_router=DefaultRouter()
course_router.register('',CourseViewSet,basename='course')

tag_router=DefaultRouter()
tag_router.register('',TagViewSet,basename='tag')

urlpatterns = [ 

   
   path('slug/<str:slug>/',CourseSlugDetailView.as_view(), name='course-detail-by-slug'),
   path('categories/slug/<str:slug>/',CategorySlugDetailView.as_view(), name='category-detail-by-slug'),
   path('categories/',include(category_router.urls)),   
   path('categories/<str:category_id>/courses/',CoursesByCategoryView.as_view(),name='courses-by-category'),   
   path('tags/',include(tag_router.urls)),
   
   path('courses/',include(course_router.urls)),


   # path('categories',CategoryViewSet.as_view(),name='category-list-api'),
   # path('categories/<str:pk>',CategoryDetailView.as_view(),name='category-detail-api'),
]
