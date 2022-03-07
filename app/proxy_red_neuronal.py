import requests
from app import constants

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
    body = {
        "base64Image": image,
        "nn_model":"InceptionV3"
    }
    response =  requests.post(constants.URL_RED_NEURONAL,json=body)
    if response.status_code != 200:
        return {"satsus":"Error"}
    return response.json()