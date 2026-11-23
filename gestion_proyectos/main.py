from datos.conexion import db
from datos.modelos.usuario import Usuario
from datos.modelos.proyecto import Proyecto
from datos.modelos.lista import Lista
from datos.modelos.tarea import Tarea
from presentacion.menu_login import mostrar_menu_login
from presentacion.menu_principal import mostrar_menu_principal

def inicializar_base_datos():
    db.connect()
    db.create_tables([Usuario, Proyecto, Lista, Tarea])
    print("✅ Base de datos inicializada correctamente")

if __name__ == "__main__":
    inicializar_base_datos()
    usuario_actual = mostrar_menu_login()
    if usuario_actual:
        mostrar_menu_principal(usuario_actual)
