from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from doubtapp.models import *
from doubtapp.serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import BasePermission


# Create your views here.

class canDeleteAndUpdateOnlyOwnDoubt(BasePermission):
    def has_permission(self, request, view):
        method=request.method
        if method in ['PUT','DELETE','PATCH']:
            user=request.user
            if user.is_superuser:
                return True
            
            doubt_id=view.kwargs.get('pk')
            try:
                doubt=Doubt.objects.get(pk=doubt_id)
            except Doubt.DoesNotExist:
                return Response({"details":"doubt not found."},status=400)
            return doubt.user == user
        return True


class canDeleteAndUpdateOnlyOwnDoubtAnswer(BasePermission):
    def has_permission(self, request, view):
        method=request.method
        if method in ['PUT','DELETE','PATCH']:
            user=request.user
            if user.is_superuser:
                return True
            
            doubt_id=view.kwargs.get('pk')
            try:
                doubt=DoubtAnswer.objects.get(pk=doubt_id)
            except DoubtAnswer.DoesNotExist:
                return Response({"details":"doubt not found."},status=400)
            return doubt.user == user
        return True


class DoubtModelViewSet(ModelViewSet):
    permission_classes=[IsAuthenticatedOrReadOnly,canDeleteAndUpdateOnlyOwnDoubt]
    queryset=Doubt.objects.all()
    serializer_class=DoubtSerializer


class DoubtAnswerModelViewSet(ModelViewSet):
    permission_classes=[IsAuthenticatedOrReadOnly,canDeleteAndUpdateOnlyOwnDoubtAnswer]
    queryset=DoubtAnswer.objects.all()
    serializer_class=DoubtAnswerSerializer
    filterset_fields='__all__'