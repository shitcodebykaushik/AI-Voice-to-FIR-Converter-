from django.urls import path
from .views import (
    upload_audio,
    convert_audio_to_fir,
    get_fir_details
)
from django.conf import settings
from django.conf.urls.static import static
from .views import register_police, login_police, get_profile
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", register_police, name="register"),
    path("login/", login_police, name="login"),
    path("profile/", get_profile, name="profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Upload Audio API
    path('upload/', upload_audio, name='upload-audio'),

    # Convert Audio to FIR
    path('fir/<uuid:audio_id>/', convert_audio_to_fir,
         name='convert-audio-to-fir'),

    # Get FIR Details by Case ID
    path('fir/<str:case_id>/', get_fir_details, name='get-fir-details'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
