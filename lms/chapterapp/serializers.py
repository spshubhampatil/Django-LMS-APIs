from .models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import traceback


def changeChapterData(instance):
    chapter_type=instance.chapter_type    
    
    if(chapter_type=='T'):
        text_chapter=instance.text_chapter
        instance.text_chapter=TextChapter(title=text_chapter.title, id=text_chapter.id)

    if(chapter_type=='L'):
        link_chapter=instance.link_chapter
        instance.link_chapter=LinkChapter(title=link_chapter.title, id=link_chapter.id)

    if(chapter_type=='V'):
        video_chapter=instance.video_chapter
        instance.video_chapter=VideoChapter(title=video_chapter.title, id=video_chapter.id)        
    
    return instance


class TextChapterSerializer(ModelSerializer):
    chapter=serializers.UUIDField(required=False)
    class Meta:
        model=TextChapter
        fields='__all__'

    def to_representation(self,instance):
        original_object= super().to_representation(instance)
        original_object.pop('chapter')
        return original_object


class HeadingChapterSerializer(ModelSerializer):
    chapter=serializers.UUIDField(required=False)
    class Meta:
        model=HeadingChapter
        fields='__all__'

    def to_representation(self,instance):
        original_object= super().to_representation(instance)
        original_object.pop('chapter')
        return original_object


class VideoChapterSerializer(ModelSerializer):
    chapter=serializers.UUIDField(required=False)
    class Meta:
        model=VideoChapter
        fields='__all__'
    

class LinkChapterSerializer(ModelSerializer):
    chapter=serializers.UUIDField(required=False)
    class Meta:
        model=LinkChapter
        fields='__all__'

    def to_representation(self,instance):
        original_object= super().to_representation(instance)
        original_object.pop('chapter')
        return original_object


class ChildChapterSerializer(ModelSerializer):
    index=serializers.IntegerField(required=False)
    heading_chapter=HeadingChapterSerializer(read_only=True)
    link_chapter=LinkChapterSerializer(read_only=True)
    text_chapter=TextChapterSerializer(read_only=True)
    video_chapter=VideoChapterSerializer(read_only=True)

    class Meta:
        model=Chapter
        fields='__all__'
    
    def to_representation(self,instance):
        all_data=self.context.get("all_data")
        if not all_data:
            instance=changeChapterData(instance)
        data = super().to_representation(instance)
        course=instance.course
        user=self.context.get('request').user
        data['is_enrolled']=course.is_user_enrolled(user)
        return data      
    

class ChapterSerializer(ModelSerializer):
    index=serializers.IntegerField(required=False)
    heading_chapter=HeadingChapterSerializer(read_only=True)
    link_chapter=LinkChapterSerializer(read_only=True)
    text_chapter=TextChapterSerializer(read_only=True)
    video_chapter=VideoChapterSerializer(read_only=True)
    child_chapters=serializers.SerializerMethodField()

    class Meta:
        model=Chapter
        fields='__all__'

    def delete_chapter_type_data(self, chapter, chapter_types_tobedelete):

        for chapter_type_tobedelete in chapter_types_tobedelete:

            try:
                if chapter_type_tobedelete=='H':
                    chapter.heading_chapter.delete()

                if chapter_type_tobedelete=='T':
                    chapter.text_chapter.delete()

                if chapter_type_tobedelete=='V':
                    chapter.video_chapter.delete()

                if chapter_type_tobedelete=='L':
                    chapter.link_chapter.delete()

            except:                
                traceback.print_exc();
     
    def delete_chapter_data(self, instance, current_chapter_type):
        chapter_types=["L","V","T","H"]
        to_be_delete_list=list(filter(lambda type: current_chapter_type != type ,chapter_types))        
        self.delete_chapter_type_data(instance,to_be_delete_list)            

    def update(self, instance, validated_data):
        chapter_type_before_update=instance.chapter_type
        chapter = super().update(instance, validated_data)

        chapter_type_object_validated_data=validated_data.get('chapter_type_object_validated_data')
        
        # chapter_type_object.save()

        chapter_type=chapter.chapter_type

        if chapter_type != chapter_type_before_update:
            #delete previous chapter
            self.delete_chapter_data(instance,chapter_type)

        if(chapter_type=='H'):
            try:
                HeadingChapterSerializer().update(chapter.heading_chapter,chapter_type_object_validated_data)
            
            except HeadingChapter.DoesNotExist:
                obj=HeadingChapter(**chapter_type_object_validated_data)  
                obj.chapter=chapter
                obj.save()                  
                chapter.heading_chapter=obj     

        if(chapter_type=='T'):
            try:
                TextChapterSerializer().update(chapter.text_chapter,chapter_type_object_validated_data)
            
            except TextChapter.DoesNotExist:
                obj=TextChapter(**chapter_type_object_validated_data)
                obj.chapter=chapter    
                obj.save()
                chapter.text_chapter=obj  

        if(chapter_type=='V'):
            try:
                VideoChapterSerializer().update(chapter.video_chapter,chapter_type_object_validated_data)
            
            except VideoChapter.DoesNotExist:
                obj=VideoChapter(**chapter_type_object_validated_data)  
                obj.chapter=chapter               
                obj.save()  
                chapter.video_chapter=obj  

        if(chapter_type=='L'):
            try:
                LinkChapterSerializer().update(chapter.link_chapter,chapter_type_object_validated_data)
            
            except LinkChapter.DoesNotExist:
                obj=LinkChapter(**chapter_type_object_validated_data)   
                obj.chapter=chapter
                obj.save() 
                chapter.link_chapter=obj     
        
        chapter.save()

        return chapter

    def validate(self, attrs):
        data=self.context.get('request').data
        chapter_type=data.get('chapter_type')
        chapter_type_object_validated_data=None
        chapter_type_object=None
        chapter_type_class=None

        if(chapter_type=='H'):
            chapter_type_object_validated_data=self.handleHeadingChapter(data)
            chapter_type_class=HeadingChapter

        if(chapter_type=='T'):
            chapter_type_object_validated_data=self.handleTextChapter(data)
            chapter_type_class=TextChapter

        if(chapter_type=='L'):
            chapter_type_object_validated_data=self.handleLinkChapter(data)
            chapter_type_class=LinkChapter

        if(chapter_type=='V'):
            chapter_type_object_validated_data=self.handleVideoChapter(data)
            chapter_type_class=VideoChapter

        chapter_type_object=chapter_type_class(**chapter_type_object_validated_data)

        attrs['chapter_type_object']=chapter_type_object
        attrs['chapter_type_object_validated_data']=chapter_type_object_validated_data
        return attrs

    def to_representation(self,instance):
        all_data=self.context.get("all_data")
        if not all_data:
            instance=changeChapterData(instance)
        data = super().to_representation(instance)
        course=instance.course
        user=self.context.get('request').user
        data['is_enrolled']=course.is_user_enrolled(user)
        return data

    def get_child_chapters(self, instance):
        childs=instance.child_chapters.all().order_by('index')
        serializer= ChildChapterSerializer(childs, many=True,context=self.context)
        return serializer.data

    def create(self,validated_data):
        chapter_type_object=validated_data['chapter_type_object']
        validated_data.pop('chapter_type_object')
        validated_data.pop('chapter_type_object_validated_data')

        chapter=Chapter(**validated_data)
        parent_chapter=validated_data.get('parent_chapter')
        course=chapter.course

        if(chapter.parent_chapter is None):
            last_index_parent_chapter=Chapter.objects.filter(course=course,parent_chapter=None).count()
            chapter.index=last_index_parent_chapter+1
            chapter.save()
            chapter_type_object.chapter=chapter
            chapter_type_object.save()

        else:
            total_childs = Chapter.objects.filter(parent_chapter=parent_chapter).count()
            chapter.index= total_childs+1
            chapter.save()
            chapter_type_object.chapter=chapter
            chapter_type_object.save()
            
        return chapter

    def handleHeadingChapter(self,raw_json):
        heading_chapter_raw= raw_json.get('heading_chapter')

        if not heading_chapter_raw:
            raise ValidationError({"heading_chapter":["heading_chapter is required."]})
        header_chapter_serializer=HeadingChapterSerializer(data=heading_chapter_raw)
        if header_chapter_serializer.is_valid():
            return header_chapter_serializer._validated_data
        else:
            raise ValidationError({"heading_chapter":header_chapter_serializer.errors})
    
    def handleTextChapter(self,raw_json):
        text_chapter_raw= raw_json.get('text_chapter')

        if not text_chapter_raw:
            raise ValidationError({"text_chapter":["text_chapter is required."]})
        text_chapter_serializer=TextChapterSerializer(data=text_chapter_raw)
        if text_chapter_serializer.is_valid():
            return text_chapter_serializer._validated_data
        else:
            raise ValidationError({"text_chapter":text_chapter_serializer.errors})

    def handleLinkChapter(self,raw_json):
        link_chapter_raw= raw_json.get('link_chapter')

        if not link_chapter_raw:
            raise ValidationError({"link_chapter":["link_chapter is required."]})
        link_chapter_serializer=LinkChapterSerializer(data=link_chapter_raw)
        if link_chapter_serializer.is_valid():
            return link_chapter_serializer._validated_data
        else:
            raise ValidationError({"link_chapter":link_chapter_serializer.errors})

    def handleVideoChapter(self,raw_json):
        video_chapter_raw= raw_json.get('video_chapter')

        if not video_chapter_raw:
            raise ValidationError({"video_chapter":["video_chapter is required."]})

        video_chapter_serializer=VideoChapterSerializer(data=video_chapter_raw)

        if video_chapter_serializer.is_valid():
            return video_chapter_serializer._validated_data
            
        else:
            raise ValidationError({"video_chapter":video_chapter_serializer.errors})