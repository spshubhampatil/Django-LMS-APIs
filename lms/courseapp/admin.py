from django.contrib import admin
from .models import *

# Register your models here.

class courseAdminModel(admin.ModelAdmin):
    model=Course
    list_editable=['active']
    list_display=['title','active']


admin.site.register(Category)
admin.site.register(Course,courseAdminModel)
admin.site.register(Tag)