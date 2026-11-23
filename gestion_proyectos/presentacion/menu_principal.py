from auxiliares.mensajes import mostrar_exito

def mostrar_menu_principal(usuario):
    while True:
        print("\n" + "="*50)
        print(f"   📂 SISTEMA DE GESTIÓN DE PROYECTOS")
        print(f"   Bienvenido, {usuario.nombre}")
        print("="*50)
        print("1. Ver mis proyectos")
        print("2. Crear nuevo proyecto")
        print("3. Salir")
        print("="*50)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("\n📋 Funcionalidad en desarrollo...")
        
        elif opcion == "2":
            print("\n➕ Funcionalidad en desarrollo...")
        
        elif opcion == "3":
            mostrar_exito("¡Sesión cerrada correctamente!")
            break
        
        else:
            print("❌ Opción no válida")
