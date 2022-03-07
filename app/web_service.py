from app import app
from app.proxy_red_neuronal import red_neuronal
from app import  constants
@app.route("/ejemplo")
def ejempo_red_neuronal():
    """Funcion de ejemplo para el funcionaminto de la red neuronal
    
    Returns:
        response: respuesta de la solicitud
    """
    return red_neuronal(constants.IMAGEN)