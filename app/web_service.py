import base64
from logging import error
from time import strptime
from flask_cors import cross_origin
import numpy as np
import cv2


from app.proxy_red_neuronal import red_neuronal
from flask import flash, jsonify, request, flash, make_response, session,current_app
from app import constants
from flask_login import login_user, login_required, logout_user

from app import login_manager
from app.models import *
from werkzeug.security import check_password_hash

from app import application
from services.reszie_imge import image_resize_average_color


@login_manager.user_loader
def load_user(user_name):
    return Usuario.get_user(user_name)

@application.route("/")
def inicio():
    return "hola"
@application.route("/login", methods=["POST"])
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

@application.route("/logout", methods=["POST"])
@login_required
def logout():
    current_app.logger.info("Usuario {} deslogueado logueado".format(session["_user_id"]))
    logout_user()
    flash("se ha cerrado sesion")
    return make_response(jsonify({"respuesta":"cerrado"}),200)



"""
    NOTE: 
        Teacher endpoints should go into a separate controller :)
"""
@application.route("/courses", methods=["GET"])
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

@application.route("/course-sessions", methods=["GET"])
def get_course_sessions():
    req_user = request.args.get('user')
    req_course_id = request.args.get('courseId')

    if req_user == None: 
        return make_response(jsonify('Unathorized request'), 403)

    course_sessions = Usuario.get_course_sessions(req_course_id)

    response = []
    for session in course_sessions:
        class_number = session._asdict().get('clase_id')
        session_date = datetime.strftime(session._asdict().get('hora_inicio'), '%d/%b/%Y')
        state = 'Finalizado'
        session_id = session._asdict().get('sesion_id')
        response.append({"clase": class_number, "fecha": session_date, "estado": state, "id": session_id})
    # Eof

    return make_response(jsonify(response))
# Eod


@application.route("/recibir-imagen", methods=["POST"])
@login_required
def end_point_nn():
    """Funcion de ejemplo para el funcionaminto de la red neuronal

    Guardar:
        response: respuesta de la solicitud
    """

    user = Usuario.get_user(session["_user_id"])
    id_sesion_activa = user.get_actual_sesion_estudiante()
    print("nn", id_sesion_activa)
    if user.type != "estudiante":
        return make_response(jsonify("Acceso denegado"), 403)
    if id_sesion_activa ==  None:
        return make_response(jsonify("No hay sesion activa"), 400)
    re = list(request.json.values())

    nparr = np.fromstring(base64.b64decode(re[0]), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Process image
    resized_image = image_resize_average_color(image)
    _, buffer = cv2.imencode(".png", resized_image)

    image_base64 = base64.b64encode(buffer)
    resultado = red_neuronal(image_base64)
    current_app.logger.info("Calculando emocion")
    today = datetime.strptime(re[1], '%d/%m/%Y, %H:%M:%S')
    print("RE: ", re[1])
    print("today: ", today)
    Emocion_x_Estudiante.insert_emocion_estudiante(user.id,id_sesion_activa,today,resultado["data"]["prediction"],resultado["data"]["label_confidence"])
    return make_response(jsonify(resultado),200)

@application.route("/info_sesion",methods=["GET"])
@login_required
def obtener_info_sesion():
    id = request.args.get('id')
    
    try:
        #La sesión la envía el historial.
        resultado = Emocion_x_Estudiante.get_emocions_for_sesion(id)
        current_app.logger.info(f"solicitud de sesion {id}")
        if len(resultado) == 0:
            return make_response(jsonify({"error":"no data"}),400)
        horas =  set()
        estudiantes = set()
        data = []
        for r in resultado:
            d = {}
            d["nombre"] = r["name"] + " "+ r["last_name"]
            
            estudiantes.add(
                d["nombre"]
            )
            d["emocion"] = r["nombre"]
            d["fecha"] =  str(r["fecha"])
            horas.add(str(r["fecha"]))
            
            data.append(d)
        horas = list(horas)
        horas.sort(key= lambda date: datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
        print("estudiantes" , estudiantes)
        response = {
            "dates" : horas,
            "data":data,
            "students": list(estudiantes)
        }
        
        return make_response(jsonify(response), 200) 
    except Exception as err:
        print("error: ",err)
        return make_response(jsonify({"error":f"{err}"}),400)


    
@application.route("/resultado", methods=['GET'])
@login_required
def get_resultados():
    user = Usuario.get_user(session["_user_id"])
    id_sesion_activa = user.get_actual_sesion_profesor()
    print("sesion_activa: " , id_sesion_activa)
    list = []
    if id_sesion_activa == None:
        print("NONE")
        resultado = "No hay sesions activas"
        info = {'status': 1}
        list.append(info)
    else:
        resultado = Emocion_x_Estudiante.get_emocion_x_estudiante(id_sesion_activa)        
        for ex in resultado:
            porcentaje = ex[4] * 100
            info = { 'emocion_id' : ex[3], 'sesion_id' : ex[1], 'porcentaje': porcentaje, 'estudiante_id' : ex[0], 'fecha' : ex[2], 'status' : 0 }
            list.append(info)
            info = {}
    print("List: ", list)
    print("resultado: ", resultado)
    #TO DO... don't duplicate students count
    return jsonify(list)
