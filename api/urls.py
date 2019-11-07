from django.conf.urls import url
from .views import create_check, new_checks, check

urlpatterns = [
    url(r'^create_check/',  create_check),
    url(r'^new_checks/', new_checks),
    url(r'^check/', check)
]