from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from courseapp.models import Course
from orderapp.models import Subscription
from reviewapp.serializers import ReviewSerializer
from reviewapp.models import Review
from rest_framework.permissions import BasePermission, IsAuthenticated

# Create your views here.
class CanAddOwnReview(BasePermission):
    def has_permission(self, request, view):

        if request.method =="POST":
            logged_in_user=str(request.user.pk)
            body_user=request.data.get('user')
            if logged_in_user != body_user:
                raise ValidationError({"user":"user is not valid."})       

            return super().has_permission(request, view)
        return True


class CanAddOrUpdateReviewOnEnrolledCourseOnly(BasePermission):
    def has_permission(self, request, view):
        method=request.method
        if method in ['PUT','POST']:        
            user=request.user
            course_pk=request.data.get('course')

            if method=="POST":
                message={"course":"you are not enrolled in this course."}

            if method=="PUT":
                message={"course":"you are not enrolled in this course."}    

            if user.subscriptions.filter(course=Course(pk=course_pk)).count() == 0:
                raise ValidationError(message)

        return True
        # return super().has_permission(request, view)


class CanDeleteOwnReview(BasePermission):
    def has_permission(self, request, view):
        if request.method=="DELETE":
            review_pk= view.kwargs.get('pk')
            if Review.objects.filter(pk=review_pk,user=request.user).count() == 0:
                raise ValidationError({"details":"you are not authorized to delete this review."})
        return True


class ReviewViewSet(ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[(IsAuthenticated & CanAddOwnReview), 
                        (IsAuthenticated & CanAddOrUpdateReviewOnEnrolledCourseOnly),
                        (IsAuthenticated & CanDeleteOwnReview)
                        ]