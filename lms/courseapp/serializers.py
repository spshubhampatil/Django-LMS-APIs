from rest_framework import serializers
from .models import *
from rest_framework.serializers import ModelSerializer


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    category=CategorySerializer(read_only=True)
    student_enrolled=serializers.SerializerMethodField()    
    class Meta:
        model = Course
        fields = '__all__'

    def get_student_enrolled(self,instance):
        return instance.get_enrolled_student_count()

    
    def to_representation(self, instance):
        data= super().to_representation(instance)
       
        request=self.context.get('request')
        user=request.user
        course=instance
        data['is_enrolled']=course.is_user_enrolled(user)
        return data


class TagSerializer(ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'
