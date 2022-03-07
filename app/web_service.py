from app import app
from app.proxy_red_neuronal import red_neuronal
from app import  constants
from app.models import savebyjson
@app.route("/ejemplo")
def ejempo_red_neuronal():
    """Funcion de ejemplo para el funcionaminto de la red neuronal
    
    Guardar:
        response: respuesta de la solicitud
    """
    guardar= red_neuronal(constants.IMAGEN)
    return savebyjson(guardar)

