"""Views to zero points page and camera visualization with cookies detected."""

from django.http import HttpResponse
from django.shortcuts import render
from zero_points.models import get_points, get_image_with_circles
title = 'Puntos cero'

def home_page(request):
    """Principal page to Zero points"""
    
    data={'title':title,
        'file_html':'home.html'}
    return render(request, 'zero_points.html', context=data)

def description(request):
    """Description about the zero points"""
    
    data={'title':title,
        'subtitle':'¿Cómo funciona?',
        'file_html':'description.html'}
    return render(request, 'zero_points.html', context=data)

def our_application(request):
    """About our application of zero points with 
    artificial vision and in our project"""
    
    data={'title':title,
        'subtitle':'Nuestra Aplicación con Visión Artificial',
        'file_html':'our_application.html'}
    return render(request, 'zero_points.html', context=data)

def vizualice_camera_with_points(request):
    """Displays the image with the circles 
    drawn over the detected cookies."""

    # Ratio to convert from px to mm
    ratio_convertion = 769 / 300 # width of the bed in px from camera / width of the bed in mm on IRL
    image_url = get_image_with_circles(ratio_convertion, 30)

    data={'title':title,
    'subtitle':'Cámara con puntos cero localizados',
    'file_html':'camera.html',
    'image':image_url}
    return render(request, 'zero_points.html', context=data)

def points(request):
    """Only for test"""

    # Ratio to convert from px to mm
    ratio_convertion = 769 / 300 # width of the bed in px from camera / width of the bed in mm on IRL

    # Diameter in mm
    diameter = 30

    zero_point, zero_points = get_points(ratio_convertion, diameter)
    return HttpResponse(f"Zero point: {zero_point} \n Data points: {zero_points}")