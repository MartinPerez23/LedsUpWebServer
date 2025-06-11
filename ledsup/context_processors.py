from .models import UserConnectionStatus

def estado_conectado(request):
    if request.user.is_authenticated:
        try:
            conectado = UserConnectionStatus.objects.get(user=request.user).connected
        except UserConnectionStatus.DoesNotExist:
            conectado = False
    else:
        conectado = False

    return {"estado_conectado": conectado}
