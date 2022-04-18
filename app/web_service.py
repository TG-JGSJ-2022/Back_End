import base64
import imp
import numpy as np
import cv2


from app.proxy_red_neuronal import red_neuronal
from flask import flash, jsonify, request, flash, make_response, session,current_app
from app import constants
from flask_login import login_user, login_required, logout_user

from app import login_manager
from app.models import *
from werkzeug.security import check_password_hash

from app import app
from services.reszie_imge import image_resize_average_color


@login_manager.user_loader
def load_user(user_name):
    return Usuario.get_user(user_name)


@app.route("/login", methods=["POST"])
def login():

    req_username = request.json["user"]
    req_password = request.json["password"]
    user = Usuario.get_user(req_username)
    
    if user == None:
        return make_response(jsonify("Usuario no existe"), 400)

    if not check_password_hash(user.password, req_password):
        return make_response(jsonify("contraseña incorrecta"), 403)
    current_app.logger.info(f"Usuario {req_username} logueado")
    login_user(user)
    # print("usuario loggeado")
    return make_response(jsonify("usuario logueado formado"), 200)


@app.route("/logout", methods=["post"])
@login_required
def logout():
    logout_user()
    current_app.logger.info("Usuario {} deslogueado logueado".format(session["_user_id"]))
    flash("se ha cerrado sesion")
    return "cerrado"


@app.route("/recibir-imagen", methods=["POST"])
@login_required
def ejempo_red_neuronal():
    """Funcion de ejemplo para el funcionaminto de la red neuronal

    Guardar:
        response: respuesta de la solicitud
    """

    user = Usuario.get_user(session["_user_id"])
    id_sesion_activa = user.get_actual_sesion_estudiante()
    if id_sesion_activa ==  None:
        return "error"
    image_from_request = list(request.json.values())[0]

    nparr = np.fromstring(base64.b64decode(image_from_request), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Process image
    resized_image = image_resize_average_color(image)

    _, buffer = cv2.imencode(".png", resized_image)

    image_base64 = base64.b64encode(buffer)
    current_app.logger.info("Calculando emocion")
    resultado = red_neuronal(image_base64)
    Emocion_x_Estudiante.insert_emocion_estudiante(user.id,id_sesion_activa,datetime.today(),resultado["data"]["prediction"],resultado["data"]["label_confidence"])
    
    return resultado
