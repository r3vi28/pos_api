from .response import Result


def es_admin(user):
    """Verifica si el usuario autenticado tiene el rol Admin."""
    try:
        return user.perfil.rol.nombre == 'Admin'
    except Exception:
        return False


def requiere_admin(user):
    """
    Verifica que el usuario sea Admin.
    Retorna None si todo está bien, o una respuesta de error si no lo es.
    """
    if not user.is_authenticated:
        return Result.Error('Debe iniciar sesión para realizar esta acción.')
    if not es_admin(user):
        return Result.Error('No tiene permisos de administrador para realizar esta acción.')
    return None