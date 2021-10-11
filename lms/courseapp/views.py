from django.core.exceptions import ValidationError
from django.db.models import query
from .serializers import *
from .models import *
from django.http import response
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.parsers import JSONParser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from core.permissions import IsAdminUserOrReadOnly

# Create your views here.

class CategoryViewSet(ModelViewSet):
    permission_classes=[IsAdminUserOrReadOnly]
    serializer_class=CategorySerializer
    queryset=Category.objects.all()


class CategorySlugDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUserOrReadOnly]
    lookup_field='slug'
    serializer_class=CategorySerializer
    queryset=Category.objects.all()


class CourseViewSet(ModelViewSet):
    permission_classes=[IsAdminUserOrReadOnly]
    serializer_class=CourseSerializer
    search_fields=['title','description','tagline','slug']
    ordering_fields='__all__'
    filterset_fields = ['category', 'slug','id','price']
    queryset=Course.objects.filter(active=True)

    def get_queryset(self):
        tag=self.request.query_params.get('tag')
        if tag is not None:
            courses=Tag.objects.filter(tag=tag).values_list('course')
            return self.queryset.filter(pk__in=courses)
        return self.queryset
    
    
    def create(self, request, *args, **kwargs):
        course=request.data
        category_id=course.get('category_id')
        # course.pop('category_id')

        category=None
        if category_id is None:
            return Response({'category_id':['category_id is required.']},status=HTTP_400_BAD_REQUEST)
        try:
            category=Category.objects.get(pk=category_id)
        except Category.DoesNotExist or ValidationError:
            return Response({'category_id':['category_id is not valid.']},status=HTTP_400_BAD_REQUEST)
        
        context={
            "request":request
        }
        serializer=CourseSerializer(data=course,context=context)
        if(serializer.is_valid()):
            courseInstance=Course(**serializer.validated_data,category=category)
            courseInstance.save()
            return Response(CourseSerializer(courseInstance,context=context).data)

        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)


class CourseSlugDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUserOrReadOnly]
    lookup_field='slug'
    serializer_class=CourseSerializer
    queryset=Course.objects.all()


class TagViewSet(ModelViewSet):
    permission_classes=[IsAdminUserOrReadOnly]
    serializer_class=TagSerializer
    queryset=Tag.objects.all()

    def create(self, request, *args, **kwargs):
        tag= request.data
        body=tag.copy()
        course_id=tag.get('course')
        course=None
        try:
            course=Course.objects.get(pk=course_id)
        except Course.DoesNotExist or ValidationError:
            return Response({'course':['course id is invalid']})

        serializer=TagSerializer(data=tag)
        if serializer.is_valid():
            tag=Tag(**serializer.validated_data, course=course)
            tag.save()
            return Response(TagSerializer(tag).data)

        else:
            return Response(serializer.errors)


class CoursesByCategoryView(APIView):
    def get(self, request,category_id):
        try:
            courses=Course.objects.filter(category=Category(pk=category_id))
            serializer=CourseSerializer(courses,many=True)
            return Response(serializer.data)
        except ValidationError:
            return Response({"category_id":["category id is not valid."]},status=HTTP_400_BAD_REQUEST)
        
