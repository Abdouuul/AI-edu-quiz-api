from django.contrib import admin
from django.urls import path, include
from api.urls import router as api_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('api/', include(api_router.urls)),
    path('api/', include('authenticator.urls')),
]