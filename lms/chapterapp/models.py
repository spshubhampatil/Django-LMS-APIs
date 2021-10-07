from django.db import models
from courseapp.models import Course,Category,Tag
import uuid

chapter_choises=(
    ('T','TEXT'),
    ('H','HEADING'),
    ('V','VIDEO'),
    ('L','LINK')
)

chapter_choises_description=(
    ('T','Dummy text desc'),
    ('H','Dummy HEADING desc'),
    ('V','Dummy VIDEO desc'),
    ('L','Dummy LINK Desc')
)

video_platform_choises=(
    ('Y','Youtube'),
    ('V','Vimeo'),
)

# Create your models here.
class Chapter(models.Model): 
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)  
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='chapters')
    chapter_type=models.CharField(choices=chapter_choises , max_length=2)
    index=models.IntegerField(null=False)
    parent_chapter=models.ForeignKey("Chapter", on_delete=models.CASCADE,related_name='child_chapters',null=True,blank=True)

class LinkChapter(models.Model): 
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)  
    chapter=models.OneToOneField(Chapter, on_delete=models.CASCADE,related_name='link_chapter')
    title=models.CharField( max_length=30)
    url=models.URLField(max_length=200)

class HeadingChapter(models.Model): 
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)  
    chapter=models.OneToOneField(Chapter, on_delete=models.CASCADE,related_name='heading_chapter')
    title=models.CharField( max_length=30)
    
class TextChapter(models.Model): 
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)  
    chapter=models.OneToOneField(Chapter, on_delete=models.CASCADE,related_name='text_chapter')
    title=models.CharField( max_length=30)
    content=models.TextField(max_length=10000)


class VideoChapter(models.Model): 
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)  
    chapter=models.OneToOneField(Chapter, on_delete=models.CASCADE,related_name='video_chapter')
    title=models.CharField( max_length=30)
    video_id=models.CharField( max_length=30)
    description=models.TextField(max_length=10000)
    video_platform=models.CharField(choices=video_platform_choises, max_length=2)
