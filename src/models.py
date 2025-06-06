from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):
   
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]=mapped_column (String(120), unique=True,nullable=False)
    correo: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    contraseña: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "correo": self.correo,
           
        }

class Personas(db.Model):
    __tablename__ = 'personas'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    altura: Mapped[str] = mapped_column(String(20))
    peso: Mapped[str] = mapped_column(String(20))
    genero: Mapped[str] = mapped_column(String(20))

class Vehiculos(db.Model):
    __tablename__ = 'vehiculos'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    modelo: Mapped[str] = mapped_column(String(120))
    fabricante: Mapped[str] = mapped_column(String(120))
    costo_en_creditos: Mapped[str] = mapped_column(String(50))
    longitud: Mapped[str] = mapped_column(String(50))
    tripulacion: Mapped[str] = mapped_column(String(50))
    pasajeros: Mapped[str] = mapped_column(String(50))
    capacidad_de_carga: Mapped[str]=mapped_column (String(50))
    consumibles: Mapped[str]=mapped_column(String(50))
    clase: Mapped[str]=mapped_column(String(120))

class Planetas(db.Model):
    __tablename__ = 'planetas'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    periodo_rotacion: Mapped[str] = mapped_column(String(100))
    periodo_orbital: Mapped[str] = mapped_column(String(100))
    terreno: Mapped[str] = mapped_column(String(50))
    diametro: Mapped[str] = mapped_column(String(50))
    clima: Mapped [str]= mapped_column(String(100))
    gravedad: Mapped [str]=mapped_column(String(100))
    poblacion: Mapped[str]=mapped_column(String(120))

class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    item_id: Mapped[int] = mapped_column(nullable=False)
    item_type: Mapped[str] = mapped_column(String(50), nullable=False)
