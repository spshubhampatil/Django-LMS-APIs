from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path('chapter-types/',chapter_type_view,name='chapter-type-view'),
   path('video-platforms/',video_platform_view,name='video-platform-listview'),
   path('',ChapterCreateView.as_view(),name='chapter-createview'),
   path('course/<str:course>',ChapterListView.as_view(),name='chapter-listview'),
  
]