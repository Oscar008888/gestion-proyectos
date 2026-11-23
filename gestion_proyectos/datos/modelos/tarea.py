from peewee import Model, CharField, TextField, IntegerField, ForeignKeyField, DateTimeField
from datos.conexion import db
from datos.modelos.lista import Lista
from datetime import datetime
import uuid

class Tarea(Model):
    id = CharField(primary_key=True, default=lambda: str(uuid.uuid4()))
    titulo = CharField(max_length=200)
    descripcion = TextField(null=True)
    posicion = IntegerField(default=0)
    lista = ForeignKeyField(Lista, backref='tareas', on_delete='CASCADE')
    creado_en = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'tareas'
