from django.contrib import admin
from .models import *

# Register your models here.
class ReviewAdminModel(admin.ModelAdmin):
    model=Review
    list_display=['user','course','rating']


admin.site.register(Review,ReviewAdminModel)