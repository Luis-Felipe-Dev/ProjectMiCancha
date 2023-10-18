# middleware.py

from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
        
class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Antes de procesar la solicitud
        try:
        #     if not request.user.is_authenticated and (request.path.startswith('/accounts/')):
        #         # Redirige a una ruta específica si no tiene permisos
        #         return redirect('/login')
        # except AttributeError as ex:
        #     return redirect('/login')
        # except Exception as ex:
        #     return redirect('/')
            if (request.path.startswith('/user/') or request.path.startswith('/reservation/') or request.path.startswith('/evaluated/')) and request.user.rol.id == 2:
                # Redirige a una ruta específica si no tiene permisos
                return redirect('/home/')
            if (request.path.startswith('/user/') or request.path.startswith('/establishment/') or request.path.startswith('/field_soccer/')) and request.user.rol.id == 3:
                # Redirige a una ruta específica si no tiene permisos
                return redirect('/home/')
        except AttributeError as ex:
            return redirect('/login')
        except Exception as ex:
            return redirect('/home/')

        response = self.get_response(request)
        if response.status_code == 404:
            return redirect('/home/')

        # Después de procesar la solicitud
        return response