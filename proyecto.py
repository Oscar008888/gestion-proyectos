# -*- coding: utf-8 -*-
import os

# Estructura del proyecto
archivos = {
    "datos/conexion.py": '''import os
from peewee import SqliteDatabase
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "gestion_proyectos.db")
db = SqliteDatabase(DB_NAME)

def inicializar_base_datos():
    from datos.modelos.usuario import Usuario
    from datos.modelos.proyecto import Proyecto
    from datos.modelos.lista import Lista
    from datos.modelos.tarea import Tarea
    
    db.connect()
    db.create_tables([Usuario, Proyecto, Lista, Tarea], safe=True)
    db.close()
''',

    "datos/modelos/usuario.py": '''from peewee import Model, CharField
from datos.conexion import db

class Usuario(Model):
    username = CharField(unique=True, max_length=50)
    password_hash = CharField(max_length=255)
    nombre = CharField(max_length=100)

    class Meta:
        database = db
''',

    "datos/modelos/proyecto.py": '''from peewee import Model, CharField, ForeignKeyField
from datos.conexion import db
from datos.modelos.usuario import Usuario

class Proyecto(Model):
    nombre = CharField(max_length=100)
    descripcion = CharField(max_length=255, null=True)
    usuario = ForeignKeyField(Usuario, backref='proyectos', on_delete='CASCADE')

    class Meta:
        database = db
''',

    "datos/modelos/lista.py": '''from peewee import Model, CharField, ForeignKeyField
from datos.conexion import db
from datos.modelos.proyecto import Proyecto

class Lista(Model):
    nombre = CharField(max_length=100)
    proyecto = ForeignKeyField(Proyecto, backref='listas', on_delete='CASCADE')

    class Meta:
        database = db
''',

    "datos/modelos/tarea.py": '''from peewee import Model, CharField, ForeignKeyField
from datos.conexion import db
from datos.modelos.lista import Lista

class Tarea(Model):
    titulo = CharField(max_length=100)
    descripcion = CharField(max_length=255, null=True)
    lista = ForeignKeyField(Lista, backref='tareas', on_delete='CASCADE')

    class Meta:
        database = db
''',

    "datos/repositorio/repo_usuario.py": '''from datos.modelos.usuario import Usuario
from peewee import DoesNotExist

class RepoUsuario:
    @staticmethod
    def crear(username, password_hash, nombre):
        try:
            return Usuario.create(username=username, password_hash=password_hash, nombre=nombre)
        except Exception:
            return None

    @staticmethod
    def obtener_por_username(username):
        try:
            return Usuario.get(Usuario.username == username)
        except DoesNotExist:
            return None
''',

    "datos/repositorio/repo_proyecto.py": '''from datos.modelos.proyecto import Proyecto

class RepoProyecto:
    @staticmethod
    def crear(nombre, descripcion, usuario):
        return Proyecto.create(nombre=nombre, descripcion=descripcion, usuario=usuario)

    @staticmethod
    def listar_por_usuario(usuario):
        return list(Proyecto.select().where(Proyecto.usuario == usuario))

    @staticmethod
    def obtener_por_id(proyecto_id, usuario):
        try:
            return Proyecto.get((Proyecto.id == proyecto_id) & (Proyecto.usuario == usuario))
        except Exception:
            return None

    @staticmethod
    def eliminar(proyecto):
        return proyecto.delete_instance()
''',

    "datos/repositorio/repo_lista.py": '''from datos.modelos.lista import Lista

class RepoLista:
    @staticmethod
    def crear(nombre, proyecto):
        return Lista.create(nombre=nombre, proyecto=proyecto)

    @staticmethod
    def listar_por_proyecto(proyecto):
        return list(Lista.select().where(Lista.proyecto == proyecto))

    @staticmethod
    def obtener_por_id(lista_id, proyecto):
        try:
            return Lista.get((Lista.id == lista_id) & (Lista.proyecto == proyecto))
        except Exception:
            return None

    @staticmethod
    def eliminar(lista):
        return lista.delete_instance()
''',

    "datos/repositorio/repo_tarea.py": '''from datos.modelos.tarea import Tarea

class RepoTarea:
    @staticmethod
    def crear(titulo, descripcion, lista):
        return Tarea.create(titulo=titulo, descripcion=descripcion, lista=lista)

    @staticmethod
    def listar_por_lista(lista):
        return list(Tarea.select().where(Tarea.lista == lista))

    @staticmethod
    def obtener_por_id(tarea_id, lista):
        try:
            return Tarea.get((Tarea.id == tarea_id) & (Tarea.lista == lista))
        except Exception:
            return None

    @staticmethod
    def actualizar_lista(tarea, nueva_lista):
        tarea.lista = nueva_lista
        return tarea.save()

    @staticmethod
    def eliminar(tarea):
        return tarea.delete_instance()
''',

    "auxiliares/seguridad.py": '''import bcrypt

class Seguridad:
    @staticmethod
    def hashear_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verificar_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
''',

    "auxiliares/mensajes.py": '''class Mensajes:
    @staticmethod
    def exito(texto):
        print(f"\n[ÉXITO] {texto}")

    @staticmethod
    def error(texto):
        print(f"\n[ERROR] {texto}")

    @staticmethod
    def info(texto):
        print(f"\n[INFO] {texto}")
''',

    "negocio/gestor_usuario.py": '''from datos.repositorio.repo_usuario import RepoUsuario
from auxiliares.seguridad import Seguridad

class GestorUsuario:
    def __init__(self):
        self.repo = RepoUsuario()

    def registrar_usuario(self, username, password, nombre):
        if self.repo.obtener_por_username(username):
            return False, "El nombre de usuario ya existe."
        
        password_hash = Seguridad.hashear_password(password)
        usuario = self.repo.crear(username, password_hash, nombre)
        if usuario:
            return True, "Usuario registrado exitosamente."
        return False, "Error al registrar el usuario."

    def autenticar_usuario(self, username, password):
        usuario = self.repo.obtener_por_username(username)
        if not usuario:
            return None, "Usuario o contraseña incorrectos."
        
        if Seguridad.verificar_password(password, usuario.password_hash):
            return usuario, "Autenticación exitosa."
        return None, "Usuario o contraseña incorrectos."
''',

    "presentacion/menu_login.py": '''import os
import maskpass
from negocio.gestor_usuario import GestorUsuario
from auxiliares.mensajes import Mensajes
from presentacion.menu_principal import MenuPrincipal

class MenuLogin:
    def __init__(self):
        self.gestor_usuario = GestorUsuario()

    def mostrar(self):
        while True:
            print("\n" + "="*30)
            print("   SISTEMA GESTIÓN TRELLO   ")
            print("="*30)
            print("1. Iniciar Sesión")
            print("2. Registrarse")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self._login()
            elif opcion == "2":
                self._registro()
            elif opcion == "3":
                Mensajes.info("¡Hasta luego!")
                break
            else:
                Mensajes.error("Opción inválida.")

    def _login(self):
        print("\n--- INICIO DE SESIÓN ---")
        username = input("Usuario: ").strip()
        password = maskpass.askpass(prompt="Contraseña: ", mask="*")

        usuario, msg = self.gestor_usuario.autenticar_usuario(username, password)
        if usuario:
            Mensajes.exito(msg)
            menu_principal = MenuPrincipal(usuario)
            menu_principal.mostrar()
        else:
            Mensajes.error(msg)

    def _registro(self):
        print("\n--- REGISTRO DE USUARIO ---")
        nombre = input("Nombre completo: ").strip()
        username = input("Nombre de usuario: ").strip()
        password = maskpass.askpass(prompt="Contraseña: ", mask="*")

        if not nombre or not username or not password:
            Mensajes.error("Todos los campos son obligatorios.")
            return

        exito, msg = self.gestor_usuario.registrar_usuario(username, password, nombre)
        if exito:
            Mensajes.exito(msg)
        else:
            Mensajes.error(msg)
''',

    "presentacion/menu_principal.py": '''from datos.repositorio.repo_proyecto import RepoProyecto
from datos.repositorio.repo_lista import RepoLista
from datos.repositorio.repo_tarea import RepoTarea
from auxiliares.mensajes import Mensajes

class MenuPrincipal:
    def __init__(self, usuario):
        self.usuario = usuario

    def mostrar(self):
        while True:
            print(f"\n======== BANCO DE PROYECTOS (Usuario: {self.usuario.nombre}) ========")
            proyectos = RepoProyecto.listar_por_usuario(self.usuario)
            if not proyectos:
                print("[No tienes proyectos creados]")
            else:
                for p in proyectos:
                    print(f"ID: {p.id} | Nombre: {p.nombre} - {p.descripcion or ''}")

            print("\n1. Crear Proyecto  2. Ver/Gestionar Proyecto  3. Eliminar Proyecto  4. Cerrar Sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self._crear_proyecto()
            elif opcion == "2":
                self._gestionar_proyecto()
            elif opcion == "3":
                self._eliminar_proyecto()
            elif opcion == "4":
                break
            else:
                Mensajes.error("Opción inválida.")

    def _crear_proyecto(self):
        nombre = input("Nombre del proyecto: ").strip()
        descripcion = input("Descripción: ").strip()
        if nombre:
            RepoProyecto.crear(nombre, descripcion, self.usuario)
            Mensajes.exito("Proyecto creado.")
        else:
            Mensajes.error("El nombre es requerido.")

    def _eliminar_proyecto(self):
        pid = input("ID del proyecto a eliminar: ")
        proyecto = RepoProyecto.obtener_por_id(pid, self.usuario)
        if proyecto:
            RepoProyecto.eliminar(proyecto)
            Mensajes.exito("Proyecto eliminado.")
        else:
            Mensajes.error("Proyecto no encontrado.")

    def _gestionar_proyecto(self):
        pid = input("ID del proyecto a ver: ")
        proyecto = RepoProyecto.obtener_por_id(pid, self.usuario)
        if not proyecto:
            Mensajes.error("Proyecto no encontrado.")
            return

        while True:
            print(f"\n======== TABLERO: {proyecto.nombre} ========")
            listas = RepoLista.listar_por_proyecto(proyecto)
            
            for lista in listas:
                print(f"\n📋 Lista: {lista.nombre} (ID: {lista.id})")
                tareas = RepoTarea.listar_por_lista(lista)
                if not tareas:
                    print("  [Sin tareas]")
                for t in tareas:
                    print(f"    ✔ [{t.id}] {t.titulo}: {t.descripcion or ''}")
            
            print("\n1. Crear Lista | 2. Crear Tarea | 3. Mover Tarea | 4. Eliminar Lista/Tarea | 5. Volver")
            opcion = input("Opción: ")

            if opcion == "1":
                nom_lista = input("Nombre de la lista: ").strip()
                if nom_lista: RepoLista.crear(nom_lista, proyecto)
            elif opcion == "2":
                lid = input("ID de la lista destino: ")
                lista = RepoLista.obtener_por_id(lid, proyecto)
                if lista:
                    titulo = input("Título de la tarea: ").strip()
                    desc = input("Descripción: ").strip()
                    if titulo: RepoTarea.crear(titulo, desc, lista)
                else:
                    Mensajes.error("Lista no encontrada.")
            elif opcion == "3":
                tid = input("ID de la tarea a mover: ")
                lid = input("ID de la nueva lista destino: ")
                nueva_lista = RepoLista.obtener_por_id(lid, proyecto)
                if nueva_lista:
                    tarea_encontrada = None
                    for l in listas:
                        t = RepoTarea.obtener_por_id(tid, l)
                        if t:
                            tarea_encontrada = t
                            break
                    if tarea_encontrada:
                        RepoTarea.actualizar_lista(tarea_encontrada, nueva_lista)
                        Mensajes.exito("Tarea movida.")
                    else:
                        Mensajes.error("Tarea no encontrada.")
                else:
                    Mensajes.error("Lista destino no encontrada.")
            elif opcion == "4":
                print("1. Eliminar Lista | 2. Eliminar Tarea")
                sub_op = input("Opción: ")
                if sub_op == "1":
                    lid = input("ID de la lista a borrar: ")
                    lista = RepoLista.obtener_por_id(lid, proyecto)
                    if lista: RepoLista.eliminar(lista)
                elif sub_op == "2":
                    tid = input("ID de la tarea a borrar: ")
                    for l in listas:
                        t = RepoTarea.obtener_por_id(tid, l)
                        if t: RepoTarea.eliminar(t)
            elif opcion == "5":
                break
''',

    "main.py": '''from datos.conexion import db, inicializar_base_datos
from presentacion.menu_login import MenuLogin

def main():
    inicializar_base_datos()
    try:
        db.connect(reuse_if_open=True)
        app = MenuLogin()
        app.mostrar()
    finally:
        if not db.is_closed():
            db.close()

if __name__ == "__main__":
    main()
''',

    ".env": '''DB_NAME=gestion_proyectos.db
''',

    ".gitignore": '''__pycache__/
*.py[cod]
*$py.class
.env
.venv
env/
venv/
ENV/
*.db
''',

    "README.md": '''# Sistema de Gestión de Proyectos (Estilo Trello)

Este es un sistema de gestión de proyectos por consola inspirado en el flujo Kanban de Trello, construido utilizando principios de arquitectura limpia.

## Características
- Registro y autenticación segura con hash de contraseñas.
- Creación de proyectos dinámicos por usuario.
- Organización a través de listas y tareas dentro de cada tablero.
- Capacidad de transicionar y mover tareas entre listas.

## Requisitos del Sistema
- Python 3.x
'''
}

# Generar archivos
for ruta, contenido in archivos.items():
    directorio = os.path.dirname(ruta)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"Generado: {ruta}")

print("\n[PROCESO COMPLETADO]: Toda la estructura ha sido creada exitosamente.")
