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

    response_user = {'username': user.user, 'id': user.id,
                     "rol":user.type}

    return make_response(jsonify(response_user), 200)
# Eod

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    current_app.logger.info("Usuario {} deslogueado logueado".format(session["_user_id"]))
    flash("se ha cerrado sesion")
    return "cerrado"



"""
    NOTE: 
        Teacher endpoints should go into a separate controller :)
"""
@app.route("/courses", methods=["GET"])
def get_courses(): 

    req_user = request.args.get('user')
    req_user_id = request.args.get('id')

    if req_user == None: 
        return make_response(jsonify('Unathorized request'), 403)

    teacher_courses = Usuario.get_teacher_courses(req_user_id)
    response = []
    for course in teacher_courses:
        courseId = course._asdict().get('id')
        courseName = course._asdict().get('nombre')
        response.append({'courseCode': courseId, 'courseName': courseName})

    return make_response(jsonify(response), 200) 
# Eod



@app.route("/recibir-imagen", methods=["POST"])
@login_required
def end_point_nn():
    """Funcion de ejemplo para el funcionaminto de la red neuronal

    Guardar:
        response: respuesta de la solicitud
    """

    user = Usuario.get_user(session["_user_id"])
    id_sesion_activa = user.get_actual_sesion_estudiante()
    if user.type != "estudiante":
        return make_response(jsonify("Acceso denegado"), 403)
    if id_sesion_activa ==  None:
        return make_response(jsonify("No hay sesion activa"), 400)
    image_from_request = list(request.json.values())[0]

    nparr = np.fromstring(base64.b64decode(image_from_request), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Process image
    resized_image = image_resize_average_color(image)
    _, buffer = cv2.imencode(".png", resized_image)

    image_base64 = base64.b64encode(buffer)
    resultado = red_neuronal(image_base64)
    current_app.logger.info("Calculando emocion")
    resultado = red_neuronal(image_base64)
    Emocion_x_Estudiante.insert_emocion_estudiante(user.id,id_sesion_activa,datetime.today(),resultado["data"]["prediction"],resultado["data"]["label_confidence"])
    
    return resultado


    
@app.route("/resultado", methods=['GET'])
def get_resultados():
    
    resultado = Emocion_x_Estudiante.get_emocion_x_estudiante(1)
    list = []
    dict = {}
    for ex in resultado:
        dict.update(ex.__dict__)
        dict.pop('_sa_instance_state')
        list.append(dict)
        dict = {}
    #TO DO... Timer and don't duplicate students count
    return jsonify(list)
