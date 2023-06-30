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


def load_image():
    try:
        
        # Load the image
        url = 'http://192.168.1.68:8888'
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return image
    except:
        print(Exception)
        return None
    
def get_image(ratio_convertion, diameter_in_mm = 30):

    image = load_image()
    image_path = os.path.join(MEDIA_ROOT, r'camera\image.jpg')  # Replace 'image.jpg' with your image file name
    image_url = MEDIA_URL + 'camera/image.jpg'
    if image is not None:
        zero_point, circles = get_circles(ratio_convertion, diameter_in_mm)

        zero_point = np.round(np.asarray(zero_point)).astype(int)
        circles = np.round(circles[0, :]).astype(int)

        # Draw detected circles on the original image
        for (x, y, r) in circles:
            
            print (x, y, r)
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)
            cv2.circle(image, (x, y), 1, (255, 0, 0), 2)

        cv2.circle(image, zero_point, 1, (255, 255, 0), 2)
        print("SIIIIIIIIII")
        
        # Save image
        cv2.imwrite(image_path, image)

        return image_url
    else:
        print("Nadaaaaaaaa")
        return None

def get_points(ratio_convertion, diameter_in_mm = 30):

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

    image = load_image()

    if image is not None:

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Calculate prom radius in px from the diameter in mm
        radius_prom = np.round((diameter_in_mm/2) * ratio_convertion).astype(int)

        # Zero point (example for 800x600 image)
        x_px, y_px, _ = image.shape
        zero_point = (x_px - 400, y_px -435) #x , y (inverted)

        # Apply Hough Circle Transform
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT_ALT, 1, 50,
                                param1=100, param2=0.6, minRadius=radius_prom-5, maxRadius=radius_prom+5)

        # Return circles
        return zero_point, circles
    else:
        return None

"""
def get_points_with_AI():

    url = "http://192.168.1.68:8888"
    image = Image.open(requests.get(url, stream=True).raw)

    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # convert outputs (bounding boxes and class logits) to COCO API
    # let's only keep detections with score > 0.9

    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
    list_centers = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        print(
                f"Detected {model.config.id2label[label.item()]} with confidence "
                f"{round(score.item(), 3)} at location {box}"
        )
        center = (int((box[2]+box[0])/2),int((box[3]+box[1])/2))
        list_centers.append(center)
    return list_centers
"""