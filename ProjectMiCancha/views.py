from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appUser.models import User
from appFieldSoccer.models import FieldSoccer
from appEstablishment.models import Establishment
from appReservation.tasks import start_task
# from django.db.models import Max

# start_task()

def handle_decode_image_base64(image):
    image_decode = image.decode("utf-8")
    return image_decode

@login_required
def home(request):
    # # Obtener los identificadores únicos de establecimientos
    # unique_establishments = FieldSoccer.objects.values('establishment').annotate(max_id=Max('id')).values_list('max_id', flat=True)
    # # Obtener los registros de FieldSoccer para esos establecimientos
    # field_soccer_all = FieldSoccer.objects.filter(id__in=unique_establishments).values('id', 'name', 'number_players', 'price', 'image_base64', 'establishment')
    
    field_soccer_all = []
    
    establishment = Establishment.objects.filter(type_dist=request.user.type_dist.id)
    field_soccer_temp = FieldSoccer.objects.filter(establishment__in=establishment)

    for field in field_soccer_temp:
        field.number_players = f'{round(field.number_players / 2)} vs {round(field.number_players / 2)}'
    
    for image in field_soccer_temp:
        field_soccer_all.append((image, handle_decode_image_base64(image.image_base64)))

    field_soccer_count = FieldSoccer.objects.filter(establishment__in=establishment).count()
    field_soccer_all_count = FieldSoccer.objects.count()

    context = {
        'field_soccer_all': field_soccer_all,
        'field_soccer_count': field_soccer_count,
        'field_soccer_all_count': field_soccer_all_count
    }
    return render(request, 'home.html', context)

def login_custom(request):
    message = ''

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None and user.status == 1:
            try:
                login(request, user)
                return redirect("/home/")
            except Exception as ex:
                context = {
                   'result': False
                }
                return render(request, 'registration/login.html', context)
        else:
            context = {
                'result': False
            }
            return render(request, 'registration/login.html', context)

        # if user is not None:
        #     login(request, user)
        #     return redirect("/")
        # else:
        #     message = 'El usuario no existe o la contraseña es incorrecta.'
        #     messages.add_message(request, messages.INFO, message)
        #     return redirect("/login")
    else:
        return render(request, "registration/login.html")
    
def change_password(request):
    if request.method == 'POST':
        user = authenticate(request, email=request.POST['email'], password=request.POST['password_current'])
        print(user)
        print(request.POST['password_current'])
        if user is not None:
            try:
                print(request.POST['password_new'])
                user_change_password = User.objects.get(email=request.POST['email'])
                user_change_password.set_password = request.POST['password_new'].strip()
                user_change_password.save()
                context = {
                   'result': True
                }
                return render(request, 'user/change_password.html', context)

            except Exception as ex:
                print(ex)
                context = {
                   'result': False
                }
                return render(request, 'user/change_password.html', context)
        else:
            context = {
                'result': False
            }
            return render(request, 'user/change_password.html', context)

    else:
        return render(request, 'user/change_password.html')