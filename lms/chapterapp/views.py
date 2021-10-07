from .serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,CreateAPIView,ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .models import *
from core.permissions import IsAdminUserOrReadOnly
import uuid

# Create your views here.
@api_view(['GET'])
def chapter_type_view(request):

    def SearchDescription(id):
        for _id, description in chapter_choises_description:
            if id == _id:
                return description
    
    types=map(lambda e:dict(id=e[0],type=e[1],description=SearchDescription(e[0])),chapter_choises)
    return Response(types)


@api_view(['GET'])
def video_platform_view(request):   
        
    platforms=map(lambda video_platform:dict(id=video_platform[0],platform=video_platform[1]),video_platform_choises)
    return Response(platforms)


class ChapterListView(ListAPIView):
    queryset=Chapter.objects.all()
    serializer_class=ChapterSerializer
    ordering=['index']

    def get(self, request, *args, **kwargs):
        try:
            course=self.kwargs.get('course')
            uuid.UUID(course)            
        except:
            return Response({"course":["course id is not valid."]}, status=status.HTTP_400_BAD_REQUEST)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        course=self.kwargs.get('course')            
        return Chapter.objects.filter(parent_chapter=None, course=Course(pk=course)) 
        

class ChapterCreateView(CreateAPIView):
    permission_classes=[IsAdminUser]
    queryset=Chapter.objects.all()
    serializer_class=ChapterSerializer

    # def get_queryset(self):
    #     return Chapter.objects.filter(parent_chapter=None)    

    def get_serializer(self,*args, **kwargs):        
        request=self.request
        serializer= self.serializer_class(data=request.data, context={"request":request})
        serializer.is_valid()
        return serializer
        