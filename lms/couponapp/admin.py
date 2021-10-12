from django.contrib import admin
from .models import *

# Register your models here.

class CouponAdminModel(admin.ModelAdmin):
    model=Coupon
    list_display=['code','course','discount','active']

admin.site.register(Coupon,CouponAdminModel)