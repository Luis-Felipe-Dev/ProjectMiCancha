# middleware.py

from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
        
class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Antes de procesar la solicitud
        if not request.user.is_authenticated and request.path.startswith('/login'):
            print("User no autenticado")
            return redirect('/')
        else:
            try:
                if (request.path.startswith('/user/') or request.path.startswith('/reservation/create/')) and request.user.rol.id == 2:
                    print("User Propietario")
                    return redirect('/home/')
                if (request.path.startswith('/user/') or request.path.startswith('/establishment/') or request.path.startswith('/field_soccer/')) and request.user.rol.id == 3:
                    print("User Cliente")
                    return redirect('/home/')
            except AttributeError as ex:
                print(f"AttributeError: {ex}")
                return redirect('/login')
            except Exception as ex:
                print(f"Exception: {ex}")
                return redirect('/home/')
            
        response = self.get_response(request)

        if response.status_code == 404:
            return redirect('/home/')

        # Después de procesar la solicitud
        return response