from datos.modelos.tarea import Tarea

class RepositorioTarea:
    @staticmethod
    def crear(titulo, descripcion, posicion, lista):
        return Tarea.create(
            titulo=titulo,
            descripcion=descripcion,
            posicion=posicion,
            lista=lista
        )

    @staticmethod
    def obtener_por_lista(lista):
        return list(Tarea.select().where(Tarea.lista == lista).order_by(Tarea.posicion))

    @staticmethod
    def obtener_por_id(tarea_id):
        try:
            return Tarea.get(Tarea.id == tarea_id)
        except Tarea.DoesNotExist:
            return None

    @staticmethod
    def actualizar(tarea, **datos):
        for clave, valor in datos.items():
            setattr(tarea, clave, valor)
        tarea.save()
        return tarea

    @staticmethod
    def eliminar(tarea):
        return tarea.delete_instance()
