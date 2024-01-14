from django.urls import path

from zero_points.views import home_page, description, points, vizualice_camera_with_points

urlpatterns = [
    path("", home_page, name="Nuestra aplicación"),
    path("description/", description, name="description"),
    path("get/", points, name="get_points"),
    path("gcode/", vizualice_camera_with_points, name="gcode")
    
]