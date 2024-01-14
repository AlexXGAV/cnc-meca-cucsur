from django.urls import path
from marlin_control.views import home


urlpatterns = [
    path('', home, name="cnc"),
]