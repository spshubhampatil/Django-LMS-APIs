from django.contrib import admin
from django.urls import path,include
from core.views import api_root
from orderapp.urls import Orderurls,Subscriptionurls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root,name='api-root'),
    path('api/', api_root,name='api_root'),
    path('api/', include(('courseapp.urls','courses'),namespace='courses')),
    path('api/chapters/', include(('chapterapp.urls','chapters'),namespace='chapters')),
    path('api/coupons/', include(('couponapp.urls','coupons'), namespace='coupons')),
    path('api/doubts/', include('doubtapp.urls')),
    path('api/orders/', include((Orderurls,'orders'),namespace='orders')),
    path('api/subscriptions/', include((Subscriptionurls,'orders'),namespace='subscriptions')),
    path('api/reviews/', include(('reviewapp.urls','reviews'),namespace='reviews')),
]
