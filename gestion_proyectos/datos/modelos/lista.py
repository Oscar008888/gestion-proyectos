from peewee import Model, CharField, IntegerField, ForeignKeyField, DateTimeField
from datos.conexion import db
from datos.modelos.proyecto import Proyecto
from datetime import datetime
import uuid

class Lista(Model):
    id = CharField(primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = CharField(max_length=100)
    posicion = IntegerField(default=0)
    proyecto = ForeignKeyField(Proyecto, backref='listas', on_delete='CASCADE')
    creado_en = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'listas'
