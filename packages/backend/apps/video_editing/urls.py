from django.urls import path
from .views import VideoEditingView

urlpatterns = [
    path('process/', VideoEditingView.as_view(), name='video-process'),
]