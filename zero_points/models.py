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

IMAGE_PATH = os.path.join(MEDIA_ROOT, r'img\camera\image.jpg')
IMAGE_PATH_CIRCLES = os.path.join(MEDIA_ROOT, r'img\camera\image_circles.jpg')
URL_ONLINE_CAMERA_CNC = 'http://192.168.1.68:8888'

def load_image():
    """Get the image from the cnc online camera"""
    try:
        req = urllib.request.urlopen(URL_ONLINE_CAMERA_CNC)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return image
    except:
        print(Exception)
        return None

def save_image_camera():
    """Save the image from the cnc camera"""
    try:
        image = load_image()
        # Save image
        cv2.imwrite(IMAGE_PATH, image)
    except:
        print(Exception)
        return None

def get_image():
    """Return the saved image"""
    try:
        image = cv2.imread(IMAGE_PATH, cv2.IMREAD_COLOR)
        if image is not None:
            return image
        else:
            image = load_image()
            return image
    except:
        return None

def get_image_with_circles(ratio_convertion, diameter_in_mm = 30):
    """Return the url image with all the circles drawn 
    where the cookies were located."""
    #save_image()
    image_url = MEDIA_URL + 'img/camera/image_circles.jpg'
    image = get_image()
    if image is not None:
        zero_point, circles = get_circles(ratio_convertion, diameter_in_mm)

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
    else:
        print("nada")
        return None

def get_points(ratio_convertion, diameter_in_mm = 30):
    """Return the zero point (center of the machine) 
    and all the center points (x and y distance that 
    is needed to move the extruder) that contains the
    circles where the cookies where located."""

    zero_point, circles = get_circles(ratio_convertion, diameter_in_mm)

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
    

def get_circles(ratio_convertion, diameter_in_mm):
    """Return the zero point (center of the machine) 
    and all the circles that contains the cookies detected"""

    image = get_image()

    if image is not None:

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Calculate prom radius in px from the diameter in mm
        radius_prom = np.round((diameter_in_mm/2) * ratio_convertion).astype(int)

        # Zero point (example for 800x600 image, center of the machine)
        x_px, y_px, _ = image.shape
        zero_point = (x_px - 400, y_px -435) #x , y (inverted)

        # Apply Hough Circle Transform
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT_ALT, 1, 50,
                                param1=100, param2=0.6, minRadius=radius_prom-5, maxRadius=radius_prom+5)

        # Return circles
        return zero_point, circles

    return None
