#from transformers import DetrImageProcessor, DetrForObjectDetection
#import torch
#from PIL import Image
#import requests

import os
import urllib
import numpy as np
import cv2
from django.db import models
from cnc_meca_cucsur.settings import MEDIA_ROOT, MEDIA_URL
from django.utils.translation import gettext_lazy as _
import tempfile
import shutil
from django.core.validators import FileExtensionValidator
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid
import sys
from io import StringIO, BytesIO

IMAGE_PATH = os.path.join(MEDIA_ROOT, r'img\camera\image.jpg')
IMAGE_PATH_CIRCLES = os.path.join(MEDIA_ROOT, r'img\camera\image_circles.jpg')
GCODE_PATH_TEMP = os.path.join(MEDIA_ROOT, r'files\temp\temp_')
#URL_ONLINE_CAMERA_CNC = 'http://192.168.1.68:8888'


class Machine(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='img/machine', blank=True, null=True)
    cam_url = models.URLField(null=False, blank=False)
    ratio_convertion = models.FloatField(null=True, blank=True, default=2.0)
    x_adj_px_cam = models.IntegerField(null=True, blank=True, default=0)
    y_adj_px_cam = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = _("machine")
        verbose_name_plural = _("machines")

    def save(self, *args, **kwargs):

        if self.name and self.cam_url:
            new_image_name = f"{self.name}_"
            ext = os.path.splitext(self.image.name)[1]  # Get the image extension
            new_image_name_with_extension = f"{new_image_name}{ext}"
            self.image.name = new_image_name_with_extension
        
        super(Machine, self).save(*args, **kwargs)
    
    def __str__(self):
        names = [self.name]
        full_name = " ".join(filter(None, names))
        return full_name

class GcodeFile(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='files/gcode/original')
    machine = models.ForeignKey(Machine, on_delete = models.SET("Eliminada"))
    radius_cookie = models.FloatField()
    converted_file = models.FileField(upload_to='files/gcode/converted', blank=True, null=True, editable=False)

    class Meta:
        verbose_name = _("file")
        verbose_name_plural = _("files")

    def save(self, *args, **kwargs):
        if self.name and self.machine:
            new_file_name = f"{self.name}_{self.machine.name}"
            ext = os.path.splitext(self.file.name)[1]  # Get the image extension
            new_file_name_with_extension = f"{new_file_name}{ext}"
            self.file.name = new_file_name_with_extension
            #self.converted_file.name = "converted_"+new_file_name_with_extension

        super(GcodeFile, self).save(*args, **kwargs)
    
    def __str__(self):
        names = [self.name, self.machine.name]
        full_name = " ".join(filter(None, names))
        return full_name

def load_image(url_cam):
    """Get the image from the cnc online camera"""
    try:
        print(url_cam)
        req = urllib.request.urlopen(url_cam)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return image
    except:
        print("Error al capturar imagen:",Exception)
        return None

def save_image_camera(url_cam):
    """Save the image from the cnc camera"""
    try:
        image = load_image(url_cam)
        # Save image
        cv2.imwrite(IMAGE_PATH, image)
    except:
        print(Exception)


""" def get_image(url_cam):
    Return the saved image
    try:
        image = cv2.imread(IMAGE_PATH, cv2.IMREAD_COLOR)
        if image is not None:
            return image
        else:
            image = load_image(url_cam)
            return image
    except:
        return None """

def get_image_with_circles(ratio_convertion, diameter_in_mm = 30, x_adj_px=0, y_adj_px=135, url_cam=""):
    """Return the url image with all the circles drawn 
    where the cookies were located."""
    #save_image()
    image_url = MEDIA_URL + 'img/camera/image_circles.jpg'
    image = load_image(url_cam)
    
    if image is not None:
        try:

            cv2.imwrite(IMAGE_PATH, image)
            zero_point, circles = get_circles(image, ratio_convertion, diameter_in_mm, x_adj_px, y_adj_px)

            zero_point = np.round(np.asarray(zero_point)).astype(int)
            circles = np.round(circles[0, :]).astype(int)

            # Draw detected circles on the original image
            for (x, y, r) in circles:
                
                #print (x, y, r)
                cv2.circle(image, (x, y), r, (0, 255, 0), 2)
                cv2.circle(image, (x, y), 1, (255, 0, 0), 2)

            cv2.circle(image, zero_point, 1, (255, 255, 0), 2)
            
            # Save image
            cv2.imwrite(IMAGE_PATH_CIRCLES, image)
            print("SIIIIIIIIII")
            return image_url
        except Exception as e:
            print("Error en proceso de imagen: ", e)
    else:
        print("nada")
        return None

def get_points(ratio_convertion, diameter_in_mm = 30, x_adj_px=0, y_adj_px=0, url_cam=""):
    """Return the zero point (center of the machine) 
    and all the center points (x and y distance that 
    is needed to move the extruder) that contains the
    circles where the cookies where located."""
    image = load_image(url_cam)
    zero_point, circles = get_circles(image, ratio_convertion, diameter_in_mm, x_adj_px, y_adj_px)
    
    zero_points = []

    # Check if circles were found
    if circles is not None:
        circles = (circles[0, :])

        # Draw detected circles on the original image
        for (x, y, r) in circles:

            # Get relative distance from zero point
            x_0 = zero_point[0] - x
            y_0 = zero_point[1] - y

            # Calculate the reverse distance to travel to the zero point in mm
            x_1 = - x_0 / ratio_convertion
            y_1 = - y_0 / ratio_convertion

            # Radio px to mm
            r = r /ratio_convertion

            zero_points.append([x_1, y_1, r])

        return zero_point, zero_points
    else:
        return 0, ("No circles found.")

def get_circles(image, ratio_convertion, diameter_in_mm, x_adj_px, y_adj_px):
    """Return the zero point (center of the machine) 
    and all the circles that contains the cookies detected"""

    if image is not None:

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Calculate prom radius in px from the diameter in mm
        radius_prom = np.round((diameter_in_mm/2) * ratio_convertion).astype(int)

        # Zero point (example for 800x600 image, center of the machine)
        x_px, y_px, _ = image.shape
        zero_point = (x_px/2 - x_adj_px, y_px/2 + y_adj_px) #x , y (inverted)

        # Apply Hough Circle Transform
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT_ALT, 1, 50,
                                param1=100, param2=0.6, minRadius=radius_prom-50, maxRadius=radius_prom+50)

        # Return circles
        return zero_point, circles

    return None

def gcode_modification(gcode_file, ratio_convertion, diameter_in_mm=30, x_adj_px=0, y_adj_px=0, url_cam=""):
    image = load_image(url_cam=url_cam)
    zero_point, circles = get_circles(image, ratio_convertion, diameter_in_mm, x_adj_px, y_adj_px)
    zero_points = []
    zero_point = np.round(np.asarray(zero_point)).astype(int)
    print("punto cero", zero_point)

    # Check if circles were found
    if circles is not None:
        circles = circles[0, :]

        # Draw detected circles on the original image
        for (x, y, r) in circles:
            # Get relative distance from zero point
            x_0 = zero_point[0] - x
            y_0 = zero_point[1] - y

            # Calculate the reverse distance to travel to the zero point in mm
            x_1 = - x_0 / ratio_convertion
            y_1 = - y_0 / ratio_convertion

            # Radio px to mm
            r_1 = r / ratio_convertion

            zero_points.append([x_1, y_1, r_1])
            cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
            cv2.circle(image, (int(x), int(y)), 1, (255, 0, 0), 2)

        cv2.circle(image, (zero_point[1], zero_point[0]), 1, (255, 255, 0), 2)
        cv2.imwrite(IMAGE_PATH_CIRCLES, image)

        temp_file_path = GCODE_PATH_TEMP+f"_{str(uuid.uuid4())}"
        try:

                os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
                
                with open(temp_file_path, 'wb+') as salida_temp:
                    extrusion_diffs = []  # Store the extrusion differences for each G0/G1 line
                    last_extrusion_val = 0
                    extrusion_val = 0
                    entrada = BytesIO()
                    entrada.write(gcode_file)

                    for circle in circles:
                        entrada.seek(0)
                        last_extrusion_val = extrusion_val
                        for k, linea in enumerate(entrada):
                            #print(f"A {k}: {linea}")
                            if linea.startswith(b"G0") or linea.startswith(b"G1"):
                                coordenadas = linea.split()
                                for i, elem in enumerate(coordenadas):
                                    if elem.startswith(b"X"):
                                        x_valor = float(elem[1:])
                                        x_valor += circle[0]
                                        coordenadas[i] = bytes("X{:.3f}".format(x_valor), 'utf-8')
                                    elif elem.startswith(b"Y"):
                                        y_valor = float(elem[1:])
                                        y_valor += circle[1]
                                        coordenadas[i] = bytes("Y{:.3f}".format(y_valor), 'utf-8')
                                    elif elem.startswith(b"E"):
                                        extrusion_val = float(elem[1:])
                                        if k == 0: #extrusion_val not in extrusion_diffs and 
                                            extrusion_diffs.append(extrusion_val)
                                            last_extrusion_val = extrusion_val
                                        else: #elif j <= len(extrusion_diffs):
                                            extrusion_val += last_extrusion_val # + extrusion_diffs[j]
                                            #j+=1
                                        coordenadas[i] = bytes("E{:.3f}".format(extrusion_val), 'utf-8')
                                nueva_linea = b" ".join(coordenadas) + b'\n'
                                salida_temp.write(nueva_linea)
                                #print("nueva linea",nueva_linea)
                            else:
                                salida_temp.write(linea)

                    return temp_file_path

        except Exception as e:
            print("Error en modificacion de archivo:", e)
            return None
        #finally:
            #os.remove(temp_gcode.name)# Remove the temporary g
    else:
        print("No circles")
        return None