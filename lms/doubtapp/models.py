from django.db import models
from django.contrib.auth.models import User
from chapterapp.models import Chapter
from courseapp.models import Course
import uuid

# Create your models here.
class Doubt(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='doubts',null=False)
    chapter=models.ForeignKey(Chapter, on_delete=models.CASCADE,related_name='doubts',null=True,blank=True)
    course=models.ForeignKey(Course, on_delete=models.CASCADE,related_name='doubts',null=False)
    content=models.CharField(max_length=2000,null=False)

    def __str__(self):
        content = self.content
        if len(content)<=20:
            return content
        
        return f'{content[0:18]}...'

class DoubtAnswer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='answers',null=False)
    doubt=models.ForeignKey(Doubt, on_delete=models.CASCADE,related_name='answers',null=False)
    content=models.CharField(max_length=2000,null=False)