"""En el siguiente scrip se va a encontrar los modelos de clases para ser mapeadas 
en MySql con sqlalchemy 
"""
import app.db as db
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
)
from sqlalchemy.orm import relationship

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


class Usuario(db.Base):
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
    password = Column(String(20), nullable=False)
    name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    type = Column(String(10), nullable=False)
    #clase = relationship("clase_dictada", secondary=porfesor_x_clase)

    def __init__(self, user, password) -> None:
        self.user = user
        self.password = password


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


db.Base.metadata.create_all(db.engie)
