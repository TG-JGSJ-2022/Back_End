"""En el siguiente scrip se va a encontrar los modelos de clases para ser mapeadas 
en MySql con sqlalchemy 
"""
from shutil import ExecError
import app.db as db
from datetime import date, datetime, timedelta
from flask import current_app
#import db
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Table,
    Float,
    Time,
    Date,
    Boolean,
    insert,
    select,
)

from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

porfesor_x_clase = Table(
    "profesorXclase",
    db.Base.metadata,
    Column("profesor_id", ForeignKey("usuario.id"), primary_key=True),
    Column("clase_id", ForeignKey("clase.id"), primary_key=True),
)
estudiante_x_clase = Table(
    "estudianteXclase",
    db.Base.metadata,
    Column("estudiante_id", ForeignKey("usuario.id"), primary_key=True),
    Column("clase_id", ForeignKey("clase.id"), primary_key=True),
)


class Usuario(UserMixin, db.Base):
    """
    Clase usuario, dentro de esta clase se
    encuentra el valor type el cual ayuda a
    identificar si el usuario es profesor o estudiante
    Args:
        db (declarative_base): permite realizar el mapeo a la base de datos
    """

    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True)
    user = Column(String(20), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    type = Column(String(10), nullable=False)
    
    authenticated = Column(Boolean, default=False)
   
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.user

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def create_user(user, password, name, last_name, type_user):
        with db.engie.connect() as connection:
            connection.execute(
                insert(Usuario).values(
                    user=user,
                    password=generate_password_hash(password),
                    name=name,
                    last_name=last_name,
                    type=type_user,
                )
            )
            connection.close()
            

    def get_user(user):
        with db.Session.begin() as session:
            response = session.query(Usuario).where(Usuario.user == user).first()
            session.close()
        return response
    # Eod

    def get_teacher_courses(user_id):

        query = """select * 
                   from curso
                   where id in (
                       select curso_id 
                       from clase 
                       where id in (
                           select clase_id 
                           from profesorXclase, usuario 
                           where profesorXclase.profesor_id = {} and usuario.id = {}
                       )
                   );""".format(user_id, user_id)

        with db.engie.connect() as connection: 
            result = connection.execute(query)
        # Eow

        return result.all()
    # Eod

    def get_actual_sesion_estudiante(self):
        with db.engie.connect() as connection:
            result = connection.execute(
                """select bd_tesis.sesion.id,bd_tesis.sesion.hora_inicio,bd_tesis.sesion.hora_fin,dia 
                from bd_tesis.estudianteXclase,bd_tesis.clase,bd_tesis.horario,bd_tesis.sesion 
                where
                bd_tesis.estudianteXclase.estudiante_id = {} and 
                bd_tesis.clase.id = bd_tesis.estudianteXclase.clase_id and 
                bd_tesis.horario.clase_id =  bd_tesis.clase.id and
                bd_tesis.sesion.clase_id = bd_tesis.clase.id;""".format(
                    self.id
                )
            )
        # today = datetime.today()
        today = datetime(2022, 1, 28, 14,30)
        for row in result.fetchall():
            if row["hora_inicio"] <  today < row["hora_fin"]:
                return row["id"]
                
        return None

class Curso(db.Base):
    """
    Clase curso, contiene la informacion
    necesaria para identificar un curso
    Args:
        db (declarative_base): permite realizar el mapeo a la base de datos
    """

    __tablename__ = "curso"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False)
    fecha_inicio_semestre = Column(Date, nullable=False)
    fecha_fin_semestre = Column(Date, nullable=False)


class Clase(db.Base):
    """
    Contiene la informacion
    necesaria para identificar un clase
    Args:
        db (declarative_base): permite realizar el mapeo a la base de datos
    """

    __tablename__ = "clase"

    id = Column(Integer, primary_key=True)
    cantidad_estudiantes = Column(Integer)
    curso_id = Column(Integer, ForeignKey("curso.id"))


class Emocion(db.Base):
    """
    Clase emocion, contiene la informacion
    necesaria para identificar las diferentes emociones,
    esto permitira almacenar de mejor manera las emociones y tener mas
    control de cuales son
    Args:
        db (declarative_base): permite realizar el mapeo a la base de datos
    """

    __tablename__ = "emocion"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(10), nullable=False)


class Sesion(db.Base):
    """
    Clase sesion, contiene la informacion
    necesaria para identificar una sesion
    Args:
        db (declarative_base): permite realizar el mapeo a la base de datos
    """

    __tablename__ = "sesion"

    id = Column(Integer, primary_key=True)
    hora_inicio = Column(DateTime, nullable=False)
    hora_fin = Column(DateTime, nullable=False)
    clase_id = Column(Integer, ForeignKey("clase.id"))
    
    def get_sesion(id):
        with db.Session.begin() as session:
            response = session.query(Sesion).where(Sesion.id == id).first()
            session.close()
        return response
    


class Emocion_x_Estudiante(db.Base):
    """
    Clase Emocion_x_Estudiante, contiene la informacion
    necesaria para identificar el tiempo, la emoción y la sesion a la cual el
    estudiante dío la información de la emoción
    Args:
        db (declarative_base): permite realizar el mapeo a la base de datos
    """

    __tablename__ = "emocionXestudiante"

    estudiante_id = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    sesion_id = Column(Integer, ForeignKey("sesion.id"), primary_key=True)
    fecha = Column(DateTime, primary_key=True)
    emocion_id = Column(Integer, ForeignKey("emocion.id"), primary_key=True)
    porcentaje = Column(Float)

    def get_emocion_x_estudiante(sesion_id):
        with db.engie.connect() as connection:
            now = datetime.today()
            # time_d = 10
            # if now.second < time_d:             
            #     seconds = now.second + (60 - time_d)
            #     if now.minute == 0:
            #         minutes = now.minute + (60 - 1)
            #         hours = now.hour - 1
            #         previous = now.replace(second = seconds, minute= minutes, hour = hours)
            #     minutes = now.minute - 1
            #     previous = now.replace(second = seconds, minute= minutes)
            # else:
            #     seconds = now.second - time_d
            #     previous =now.replace(second = seconds)
            second_before = int(str(now.second)[0]+"0")
            second_after = int(str(now.second)[0]+"0") + 10
            before = datetime(year=now.year,month=now.month,day=now.day,hour=now.hour,minute=now.minute, second=second_before)
            previous = datetime(year=now.year,month=now.month,day=now.day,hour=now.hour,minute=now.minute, second=second_after-1)
            respuesta = connection.execute("""
                                           SELECT * FROM bd_tesis.emocionXestudiante where bd_tesis.emocionXestudiante.sesion_id = {} and (bd_tesis.emocionXestudiante.fecha between '{}' and '{}');
                            """.format(sesion_id, before - timedelta(seconds=10), previous -timedelta(seconds=10)))
            connection.close()
        return respuesta.fetchall()

    def insert_emocion_estudiante(estudiante_id,sesion_id,fecha,emocion,porcentaje):
        second = int(str(fecha.second)[0]+"0")
        new_fecha =datetime(year=fecha.year,month=fecha.month,day=fecha.day,hour=fecha.hour,minute=fecha.minute, second=second)
        try:
            with db.engie.connect() as connection:
                respuesta = connection.execute(""" 
                                select id 
                                from bd_tesis.emocion where emocion.nombre = '{}';
                                """.format(emocion))
                emocion_id = respuesta.fetchone()["id"]
                connection.execute(
                    insert(Emocion_x_Estudiante).values(
                        estudiante_id=estudiante_id,
                        sesion_id=sesion_id,
                        fecha=fecha,
                        emocion_id=emocion_id,
                        porcentaje=porcentaje,
                    )
                )
                connection.close()
        except Exception as err:
            current_app.logger.error("Error en guardar la emocion del estudiante")
    def get_emocions_for_sesion(sesion_id):
        try:
            with db.engie.connect() as connection:
                respuesta =  connection.execute("""
                                                select  bd_tesis.usuario.name,  bd_tesis.usuario.last_name,bd_tesis.emocion.nombre,bd_tesis.emocionXestudiante.fecha  
                                                from bd_tesis.emocionXestudiante,bd_tesis.emocion,bd_tesis.usuario 
                                                where 
                                                bd_tesis.emocionXestudiante.sesion_id = {} and 
                                                bd_tesis.emocionXestudiante.estudiante_id = bd_tesis.usuario.id and 
                                                bd_tesis.emocionXestudiante.emocion_id = bd_tesis.emocion.id ;""".format(sesion_id))
            return respuesta.fetchall()
        except Exception as err:
            current_app.logger.error("Error al traer los datos")
            

class Horario(db.Base):
    """
    Clase horari, contiene la informacion
    necesaria para identificar los horarios que puede tener una clase
    Args:
        db (declarative_base): permite realizar el mapeo a la base de datos
    """

    __tablename__ = "horario"

    clase_id = Column(Integer, ForeignKey("clase.id"), primary_key=True)
    dia = Column(String(15), primary_key=True)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)


#db.Base.metadata.create_all(db.engie)
# Usuario.create_user(user="simondavila",password="Banfield2019",name="Simon",last_name="Davila",type_user="estudiante")
# #print(Usuario.get_user("uzsdg4"))
