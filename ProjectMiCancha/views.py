from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appUser.models import User

@login_required
def home(request):
    return render(request, 'home.html')

def login_custom(request):
    message = ''

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None and user.status == 1:
            try:
                login(request, user)
                return redirect("/home")
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
        user = authenticate(email=request.POST['username'], password=request.POST['password_current'])
        if user is not None:
            try:
                user_change_password = User.objects.get(email=request.POST['username'])
                user_change_password.set_password = request.POST['password_new'].strip()
                user_change_password.save()
                context = {
                   'result': True
                }
                return render(request, 'user/change_password.html', context)

            except Exception as ex:
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