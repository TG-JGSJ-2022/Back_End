import requests
from app import constants
import json
def red_neuronal(image)->dict():
    """
        esta funcion se encarga establecer el llamando 
        a la red neuronal 
    Args:
        image (str): imagen en base64Image 
        
    Returns:
        dict: diccionario que contiene toda la 
            informacion de la respuesta
    """
    imageS =image.decode("utf-8")
    body = {
        "base64Image": imageS,
        "nn_model":"InceptionResNet"
    }
    response =  requests.post(constants.URL_RED_NEURONAL,json=body)
    if response.status_code != 200:
        return {"satsus":"Error"}
    return response.json()