from datos.modelos.lista import Lista

class RepositorioLista:
    @staticmethod
    def crear(nombre, posicion, proyecto):
        return Lista.create(nombre=nombre, posicion=posicion, proyecto=proyecto)

    @staticmethod
    def obtener_por_proyecto(proyecto):
        return list(Lista.select().where(Lista.proyecto == proyecto).order_by(Lista.posicion))

    @staticmethod
    def obtener_por_id(lista_id):
        try:
            return Lista.get(Lista.id == lista_id)
        except Lista.DoesNotExist:
            return None

    @staticmethod
    def actualizar(lista, **datos):
        for clave, valor in datos.items():
            setattr(lista, clave, valor)
        lista.save()
        return lista

    @staticmethod
    def eliminar(lista):
        return lista.delete_instance()
