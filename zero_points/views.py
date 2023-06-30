from django.http import HttpResponse
from django.shortcuts import render
from zero_points.models import get_points, get_image
title = 'Puntos cero'

def home_page(request):
    data={'title':title,
        'file_html':'home.html'}
    return render(request, 'zero_points.html', context=data)

def description(request):
    data={'title':title,
        'subtitle':'¿Cómo funciona?',
        'file_html':'description.html'}
    return render(request, 'zero_points.html', context=data)

def our_application(request):
    data={'title':title,
        'subtitle':'Nuestra Aplicación con Visión Artificial',
        'file_html':'our_application.html'}
    return render(request, 'zero_points.html', context=data)

def vizualice_camera_with_points(request):

    # Ratio to convert from px to mm
    ratio_convertion = 769 / 300 # width of the bed in px from camera / width of the bed in mm on IRL
    image_url = get_image(ratio_convertion, 30)

    data={'title':title,
    'subtitle':'Cámara con puntos cero localizados',
    'file_html':'camera.html',
    'image':image_url}
    return render(request, 'zero_points.html', context=data)

def points(request):
    # Ratio to convert from px to mm
    ratio_convertion = 769 / 300 # width of the bed in px from camera / width of the bed in mm on IRL

    # Diameter in mm
    diameter = 30

    zero_point, zero_points = get_points(ratio_convertion, diameter)
    return HttpResponse(f"Zero point: {zero_point} \n Data points: {zero_points}")