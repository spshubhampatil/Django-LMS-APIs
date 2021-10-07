from courseapp.models import Course
from django.db import models
import uuid
import shortuuid

# Create your models here.

def random_code():
    return shortuuid.ShortUUID().random(length=6).upper()

class Coupon(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)  
    discount=models.IntegerField()
    active=models.BooleanField(default=True)
    course=models.ForeignKey(Course, on_delete=models.CASCADE,related_name='coupons')    
    code=models.CharField(max_length=10,unique=True,null=False,default=random_code)