from datos.modelos.proyecto import Proyecto

class RepositorioProyecto:
    @staticmethod
    def crear(nombre, descripcion, usuario):
        return Proyecto.create(
            nombre=nombre,
            descripcion=descripcion,
            usuario=usuario
        )

    @staticmethod
    def obtener_por_usuario(usuario):
        return list(Proyecto.select().where(Proyecto.usuario == usuario))

    @staticmethod
    def obtener_por_id(proyecto_id):
        try:
            return Proyecto.get(Proyecto.id == proyecto_id)
        except Proyecto.DoesNotExist:
            return None

    @staticmethod
    def actualizar(proyecto, **datos):
        for clave, valor in datos.items():
            setattr(proyecto, clave, valor)
        proyecto.save()
        return proyecto

    @staticmethod
    def eliminar(proyecto):
        return proyecto.delete_instance()
