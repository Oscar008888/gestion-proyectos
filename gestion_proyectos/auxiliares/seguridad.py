import bcrypt

def hash_contraseña(contraseña: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(contraseña.encode('utf-8'), salt).decode('utf-8')

def verificar_contraseña(contraseña: str, hash_almacenado: str) -> bool:
    return bcrypt.checkpw(contraseña.encode('utf-8'), hash_almacenado.encode('utf-8'))
