from peewee import Model, CharField, DateTimeField
from datos.conexion import db
from datetime import datetime
import uuid

class Usuario(Model):
    id = CharField(primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = CharField(max_length=100)
    correo = CharField(max_length=100, unique=True)
    contraseña_hash = CharField(max_length=255)
    creado_en = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'usuarios'
