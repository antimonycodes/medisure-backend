from django.contrib import admin
from django.urls import path, include
from tracker.auth_views import signup, signin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tracker.urls')),
    path('api/auth/signup/', signup, name='signup'),
    path('api/auth/signin/', signin, name='signin'),
]