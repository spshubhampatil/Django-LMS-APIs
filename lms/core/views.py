from django.http import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

# Create your views here.
@api_view(['GET'])
def api_root(request):
    response={
        "API ROOT": reverse('api_root', request=request),

        "Course":{
            "Course List": reverse('courses:course-list', request=request),
            "Course Detail": reverse('courses:course-detail',args=[1], request=request),
            "Course Detail by Slug": reverse('courses:course-detail-by-slug',args=['course-slug'], request=request),
            "Courses by Category": reverse('courses:courses-by-category',args=['category-id'], request=request),
        },

        "Tag":{
            "Tag List": reverse('courses:tag-list', request=request),
            "Tag Detail": reverse('courses:tag-detail',args=['tag-id'], request=request),
            
        },

        "Category":{
            "Category List": reverse('courses:category-list', request=request),
            "Category Detail": reverse('courses:category-detail',args=['category-id'], request=request),
            "Category Detail by Slug": reverse('courses:category-detail-by-slug',args=['category-slug'], request=request),
        },
        "Chapter":{
            "Chapter Types":reverse('chapters:chapter-type-view',request=request),            
            "Chapter Create":reverse('chapters:chapter-createview',request=request),
            "Chapter By Course":reverse('chapters:chapter-listview',args=['course-id'],request=request),
            "Video Platform List":reverse('chapters:video-platform-listview',request=request),
        },
        "Coupon":{
            "Coupon List":reverse('coupons:coupon-list',request=request),            
            "Coupon Detail":reverse('coupons:coupon-detail',args=['coupon-id'],request=request),
            "Coupon By Code":reverse('coupons:coupon-bycode',args=['course-id','coupon-code'],request=request),
            
        } ,
        "Order":{
            "Create Order":reverse('orders:create-order',request=request),
            "Verify Order":reverse('orders:corder-verify',request=request),
        }
    }
    return Response(response)