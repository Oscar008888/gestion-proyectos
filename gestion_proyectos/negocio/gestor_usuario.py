from auxiliares.seguridad import hash_contraseña, verificar_contraseña
from datos.repositorio.repo_usuario import RepositorioUsuario

class GestorUsuario:
    @staticmethod
    def registrar(nombre: str, correo: str, contraseña: str):
        if RepositorioUsuario.obtener_por_correo(correo):
            return None, "El correo ya está registrado"
        
        hash_pass = hash_contraseña(contraseña)
        usuario = RepositorioUsuario.crear(nombre, correo, hash_pass)
        return usuario, "Usuario registrado exitosamente"

    @staticmethod
    def iniciar_sesion(correo: str, contraseña: str):
        usuario = RepositorioUsuario.obtener_por_correo(correo)
        if not usuario:
            return None, "Usuario no encontrado"
        if not verificar_contraseña(contraseña, usuario.contraseña_hash):
            return None, "Contraseña incorrecta"
        return usuario, "Inicio de sesión exitoso"
