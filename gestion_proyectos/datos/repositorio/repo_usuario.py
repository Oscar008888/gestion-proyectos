from datos.modelos.usuario import Usuario

class RepositorioUsuario:
    @staticmethod
    def crear(nombre, correo, contraseña_hash):
        return Usuario.create(
            nombre=nombre,
            correo=correo,
            contraseña_hash=contraseña_hash
        )

    @staticmethod
    def obtener_por_correo(correo):
        try:
            return Usuario.get(Usuario.correo == correo)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def obtener_todos():
        return list(Usuario.select())

    @staticmethod
    def actualizar(usuario, **datos):
        for clave, valor in datos.items():
            setattr(usuario, clave, valor)
        usuario.save()
        return usuario

    @staticmethod
    def eliminar(usuario):
        return usuario.delete_instance()
