"""En el siguiente scrip se va a encontrar los modelos de clases para ser mapeadas 
en MySql con sqlalchemy 
"""
from shutil import ExecError

from requests import session
import app.db as db
from datetime import datetime
from flask import current_app
# import db
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

    def get_clase(id):
        with db.Classs.begin() as classs:
            response = classs.query(Classs).where(Classs.id == id).first()
            classs.close()
        return response


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
    def get_sesiones_x_cursos(clase_id):
        response = db.session.query(Sesion).where(Sesion.clase_id == clase_id).all()
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
        response = db.session.query(Emocion_x_Estudiante).where(Emocion_x_Estudiante.sesion_id == sesion_id).all()
        return response
    def insert_emocion_estudiante(estudiante_id,sesion_id,fecha,emocion,porcentaje):
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


# db.Base.metadata.create_all(db.engie)
# Usuario.create_user(user="p1",password="123",name="julian",last_name="builes",type_user="profesor")
# print(Usuario.get_user("uzsdg4"))
