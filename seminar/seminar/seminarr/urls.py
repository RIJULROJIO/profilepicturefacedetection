from django.urls import path
from . import views
from django.conf import settings

from django.conf.urls.static import static


urlpatterns = [
        path('', views.home, name='home'),  # Map the root URL to the 'home' view

    
   path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
            path('check-face-detection/', views.check_face_detection, name='check_face_detection'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)