from django.urls import path
from fluidnc_control.views import home


urlpatterns = [
    path('', home, name="cnc"),
]