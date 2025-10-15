from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r"sounds", views.SoundViewSet, basename="sound")

urlpatterns = [
    path("download/", views.download, name="download"),
    path("upload/", views.upload, name="upload"),
    path("tags/", views.tags, name="tags"),
]

urlpatterns += router.urls
