from django.contrib import admin
from django.urls import path,include
from core.views import api_root,MyTokenObtainPairView
from orderapp.urls import Orderurls,Subscriptionurls
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', api_root,name='api_root'),
    path('api/', api_root,name='api_root'),
    path('api/', include(('courseapp.urls','courseapp'),namespace='courses')),
    path('api/chapters/', include(('chapterapp.urls','chapterapp'),namespace='chapters')),
    path('api/coupons/', include(('couponapp.urls','couponapp'), namespace='coupons')),
    path('api/doubts/', include(('doubtapp.urls','doubtapp'),namespace='doubts')),
    path('api/orders/', include((Orderurls,'orderapp'),namespace='orders')),
    path('api/subscriptions/', include((Subscriptionurls,'orderapp'),namespace='subscriptions')),
    path('api/reviews/', include(('reviewapp.urls','reviewapp'),namespace='reviews')),

    # Authentication Token

    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT) \
 + static(settings.STATIC_URL , document_root = settings.STATIC_ROOT)
