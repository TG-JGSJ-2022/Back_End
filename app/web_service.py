from app import app
from app.proxy_red_neuronal import red_neuronal
from flask import request
from app import  constants
import base64
import numpy as np
import cv2
from math import ceil, floor 

@app.route("/recibir-imagen", methods=['POST'])
def ejempo_red_neuronal():
    """Funcion de ejemplo para el funcionaminto de la red neuronal
    
    Returns:
        response: respuesta de la solicitud
    """
    
    image_from_request = list(request.json.values())[0]
    
    nparr = np.fromstring(base64.b64decode(image_from_request), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Process image
    resized_image = image_resize_average_color(image)

    _, buffer = cv2.imencode(".png", resized_image)

    image_base64 = base64.b64encode(buffer)

    return red_neuronal(image_base64)




###
def image_resize_average_color(image, width = 299, height = 299, inter = cv2.INTER_AREA):
    #-------------------------------------------------
    #                 Resize image
    #-------------------------------------------------
    # Initialize the dimensions of the image to be resized and grab the image size
    dim = None
    h, w, _ = image.shape

    # Calculate the ratio of the width and construct the dimensions
    r = height / float(w) if w > h else height / float(h)
    dim = (width, int(h * r)) if w > h else (int(w * r), height)

    # Resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    #-------------------------------------------------
    #            Calculate average color
    #-------------------------------------------------
    h, w, _ = resized.shape
    average_color = [0, 0, 0]
    average = h * w

    # Traverse image
    for i in range(0, h):
        for j in range(0, w):
            pixel = image[i][j]
            average_color[0] += pixel[0]
            average_color[1] += pixel[1]
            average_color[2] += pixel[2]
        # Eof
    # Eof

    average_color = list(map(lambda i : i / average, average_color))

    #-------------------------------------------------
    #  Calculate padding to add to the resized image
    #-------------------------------------------------
    # Top and bottom border
    top = ceil((299 - h) / 2) if h < 299 else 0
    bottom = floor((299 - h) / 2) if h < 299 else 0
    # Left and right border
    left = abs(ceil((299 - w) / 2)) if w < 299 else 0
    right = abs(floor((299 - w) / 2)) if w < 299 else 0

    image_with_padding = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=average_color)
    
    #-------------------------------------------------
    #      Return resized image with padding 
    #-------------------------------------------------
    return image_with_padding
# Eod
