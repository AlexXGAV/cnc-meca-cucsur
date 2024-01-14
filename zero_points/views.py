"""Views to zero points page and camera visualization with cookies detected."""

from django.http import HttpResponse
from django.shortcuts import render, redirect
from zero_points.models import get_points, get_image_with_circles, gcode_modification
from .forms import UploadFileForm
from .models import Machine, GcodeFile, IMAGE_PATH_CIRCLES
from django.core.files.uploadedfile import InMemoryUploadedFile
import os 

url_cam = ""
title = 'Nuestra aplicación'


def home_page(request):
    """Principal page to Zero points"""
    
    data={'title':title,
        'file_html':'home.html'}
    return render(request, 'zero_points.html', context=data)

def description(request):
    """About our application of zero points with 
    artificial vision and in our project"""
    
    data={'title':title,
        'subtitle':'Descripción',
        'file_html':'description.html'}
    return render(request, 'zero_points.html', context=data)


def vizualice_camera_with_points(request):
    """Displays the image with the circles 
    drawn over the detected cookies."""

    # Ratio to convert from px to mm
    #ratio_convertion = 769 / 300 # width of the bed in px from camera / width of the bed in mm on IRL
    #ratio_convertion = 600/300
    image_url = None
    #print(image_url)
    if request.method == 'POST' and 'gcode' in request.POST:
        form_gcode = UploadFileForm(request.POST, request.FILES)
        if form_gcode.is_valid():
            radius_cookie = form_gcode.cleaned_data["radius_cookie"]
            gcode_file = form_gcode.cleaned_data["file"]
            machine = form_gcode.cleaned_data["machine"]
            name_job = form_gcode.cleaned_data["name"]
            ratio_convertion = getattr(machine, "ratio_convertion")
            url_cam = getattr(machine, "cam_url")
            x_adj = getattr(machine, "x_adj_px_cam")
            y_adj = getattr(machine, "y_adj_px_cam")
            try:
                new_gcode = form_gcode.save(commit=False)
                
                converted_file_path = gcode_modification(gcode_file.read(), ratio_convertion, radius_cookie,x_adj,y_adj, url_cam)
                if converted_file_path:
                    # Open the modified file and create an InMemoryUploadedFile
                    with open(converted_file_path, 'rb') as modified_file:
                        converted_file = InMemoryUploadedFile(
                            modified_file,
                            'file',
                            f'converted_{name_job}.txt',
                            'text',
                            0,
                            None
                        )

                        # Save the converted_file to the model field
                        new_gcode.converted_file = converted_file
                        new_gcode.save()
                        form_gcode.save_m2m()
                        
                    # Remove the temporary file
                    os.remove(converted_file_path)

                return redirect("/points/gcode/?gcodeModificado")
            except Exception as e:
                print("Error final",e)
                return redirect("/points/gcode/?error2")
        else:
            print("Form is not valid:", form_gcode.errors)
    else:
        form_gcode = UploadFileForm()
    data={'title':title,
    'form':form_gcode,
    'file_html':'our_application.html',
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