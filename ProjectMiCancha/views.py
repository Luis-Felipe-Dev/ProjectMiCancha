from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appUser.models import User
from appFieldSoccer.models import FieldSoccer

@login_required
def home(request):
    field_soccer = FieldSoccer.objects.count()
    return render(request, 'home.html', {'field_soccer': field_soccer})

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