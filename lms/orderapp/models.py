from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.fields import DateTimeField
from couponapp.models import Coupon
from courseapp.models import Course
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

ORDER_STATUS_CHOISES=(
    ("S","SUCCESS"),
    ("F","FAIL"),
    ("I","INITIATED")
)


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    order_id = models.CharField(max_length=100, null=False)
    payment_id = models.CharField(max_length=100, null=True)
    order_status = models.CharField(max_length=2, default="I",choices=ORDER_STATUS_CHOISES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')         
    time=DateTimeField(auto_now_add=True)   


@receiver(post_save, sender=Order)
def createSubscription(sender, instance, **kwargs):
    order=instance

    if order.order_status!="S":
        return

    order_items=order.order_items.all()
    order_items_courses=order.order_items.all().values_list('course')

    for course in order_items_courses:
        course_pk=course[0]
        existingSubscription=None
        try:
            existingSubscription= Subscription.objects.get(user=order.user,course=Course(pk=course_pk))
        except Subscription.DoesNotExist:
            pass

        if existingSubscription is None:
            subscription =Subscription(user=order.user,order=order,course=Course(pk=course_pk))
            subscription.save()


class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='order_items')     
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')       
    price=models.IntegerField()
    discount=models.IntegerField(default=0)
    time=DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='order_items',null=True,blank=True)


class Subscription(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')     
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='subscriptions')    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    time=DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'