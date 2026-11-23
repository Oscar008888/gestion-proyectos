from peewee import Model, CharField, TextField, DateTimeField, ForeignKeyField
from datos.conexion import db
from datos.modelos.usuario import Usuario
from datetime import datetime
import uuid

class Proyecto(Model):
    id = CharField(primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = CharField(max_length=150)
    descripcion = TextField(null=True)
    usuario = ForeignKeyField(Usuario, backref='proyectos', on_delete='CASCADE')
    creado_en = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'proyectos'
