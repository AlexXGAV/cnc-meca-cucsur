from django.urls import path

from zero_points.views import home_page, description, our_application, points, vizualice_camera_with_points

urlpatterns = [
    path("", home_page, name="Puntos cero"),
    path("description/", description, name="¿Cómo funciona?"),
    path("our-application/", our_application, name="Nuestra aplicación"),
    path("get/", points, name="get_points"),
    path("camera/", vizualice_camera_with_points, name="Visualizar puntos cero")
    
]