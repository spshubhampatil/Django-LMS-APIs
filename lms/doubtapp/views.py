from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def testview(request):
    response={
        'message':'Course api is working',
        'url':request.get_full_path()
    }
    return Response(response)