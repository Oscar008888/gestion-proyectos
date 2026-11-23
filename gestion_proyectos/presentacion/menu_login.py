import maskpass
from negocio.gestor_usuario import GestorUsuario
from auxiliares.mensajes import mostrar_exito, mostrar_error

def mostrar_menu_login():
    while True:
        print("\n" + "="*40)
        print("   🔐 INICIO DE SESIÓN")
        print("="*40)
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        print("="*40)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            correo = input("Correo: ")
            contraseña = maskpass.advpass("Contraseña: ", mask="*")
            usuario, mensaje = GestorUsuario.iniciar_sesion(correo, contraseña)
            if usuario:
                mostrar_exito(mensaje)
                return usuario
            else:
                mostrar_error(mensaje)
        
        elif opcion == "2":
            nombre = input("Nombre completo: ")
            correo = input("Correo electrónico: ")
            contraseña = maskpass.advpass("Contraseña: ", mask="*")
            confirmar = maskpass.advpass("Confirmar contraseña: ", mask="*")
            
            if contraseña != confirmar:
                mostrar_error("Las contraseñas no coinciden")
                continue
            
            usuario, mensaje = GestorUsuario.registrar(nombre, correo, contraseña)
            if usuario:
                mostrar_exito(mensaje)
                return usuario
            else:
                mostrar_error(mensaje)
        
        elif opcion == "3":
            print("👋 ¡Hasta luego!")
            exit()
        
        else:
            mostrar_error("Opción no válida")
