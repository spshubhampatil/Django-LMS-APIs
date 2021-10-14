from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from courseapp.models import Course
from orderapp.models import Subscription
from reviewapp.serializers import ReviewSerializer
from reviewapp.models import Review
from rest_framework.permissions import BasePermission

# Create your views here.
class CanAddOwnReview(BasePermission):
    def has_permission(self, request, view):

        if request.method=="GET":
            return True

        logged_in_user=str(request.user.pk)
        body_user=request.data.get('user')
        if logged_in_user != body_user:
            raise ValidationError({"user":"user is not valid."})       

        return super().has_permission(request, view)


class CanAddReviewOnEnrolledCourseOnly(BasePermission):
    def has_permission(self, request, view):

        if request.method=="GET":
            return True
        
        user=request.user
        course_pk=request.data.get('course')

        if request.method=="POST":
            message={"course":"you are not enrolled in this course."}

        if request.method=="PUT":
            message={"course":"you are not enrolled in this course."}    

        if user.subscriptions.filter(course=Course(pk=course_pk)).count() == 0:
            raise ValidationError(message)

        return super().has_permission(request, view)


class ReviewViewSet(ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[CanAddOwnReview, CanAddReviewOnEnrolledCourseOnly]