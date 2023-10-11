# middleware.py

from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
        
class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Antes de procesar la solicitud
        try:
            if not request.user.is_authenticated and (request.path.startswith('/accounts/')):
                # Redirige a una ruta específica si no tiene permisos
                return redirect('/login')
        except AttributeError as ex:
            return redirect('/login')
        except Exception as ex:
            return redirect('/')

        response = self.get_response(request)
        if response.status_code == 404:
            return redirect('/')

        # Después de procesar la solicitud
        return response