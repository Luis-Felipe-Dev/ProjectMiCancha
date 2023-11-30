from django.shortcuts import render, redirect
from appUser.models import User, Rol
from typeThings.models import TypeDepartament, TypeProvince, TypeDistrict
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .utils import generate_password, send_gmail
from datetime import datetime

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


BASE_DIR = str(settings.BASE_DIR).replace("\\", "/")
STATIC_ROOT = f"{BASE_DIR}/static"

@login_required
def create(request):
    type_district = TypeDistrict.objects.filter(relation_id=127).order_by('description')
    roles = Rol.objects.all()
    message = ''

    if request.method == 'POST':
        try:
            if (len(User.objects.filter(email=request.POST['email'])) == 0):
                user_create = User()
                user_create.type_dep = TypeDepartament.objects.get(id=14)
                user_create.type_prov = TypeProvince.objects.get(id=127)
                user_create.type_dist = TypeDistrict.objects.get(id=request.POST['type_dist'])
                user_create.first_name = (request.POST['first_name']).upper().strip()
                user_create.last_name = (request.POST['last_name']).upper().strip()
                user_create.phone = request.POST['phone'].strip()
                user_create.email = request.POST['email'].strip()
                user_create.full_name_emergency_contact = request.POST['full_name_emergency_contact'].upper().strip()
                user_create.phone_emergency_contact = request.POST['phone_emergency_contact'].strip()
                user_create.rol = Rol.objects.get(id=request.POST['rol'])
                # password = generate_password()
                # user_create.set_password(password)
                user_create.set_password(request.POST['password'].strip())
                user_create.status = True
                user_create.created_user = User.objects.get(id=request.user.id).id
                user_create.save()

                # #Send Email to New Users
                # email = request.POST['email']

                # context = {
                #     'STATIC_ROOT': STATIC_ROOT,
                #     'email': email,
                #     'first_name': user_create.first_name,
                #     'last_name': user_create.last_name,
                #     'password': request.POST['password'].strip(),
                #     'mail_action': 'create'
                #     }
                
                # # Send Email
                # email_subject = 'Bienvenido a la plataforma MiCancha'
                # email_template = 'send_email/send_email_user.html'
                # email_content = render_to_string(email_template, context)
                # email = EmailMessage(
                #     email_subject,
                #     email_content,
                #     settings.EMAIL_HOST_USER,
                #     [email],
                # )
                # email.content_subtype = 'html'
                # email.send()

                return redirect("/user/")
            else:
                message = 'Email ya existe.'
                messages.add_message(request, messages.INFO, message)
                return redirect('/user/')
        except ValidationError as e:
            message = 'Algo salió mal, contacte a TI.'
            return redirect('/user/', message=message)
    else:
        context = {
            'type_district': type_district,
            'roles': roles
        }
        return render(request, 'user/create.html', context)


@login_required
def show(request):
    # pbkdf2_sha256$390000$PChAgyU2xuztZxUb0SPylU$oI7rwsLa2NFBOgjl460DZRhpPVQRJmf9qDC6xkTatjM=
    # 12345678
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'user/show.html', context)


@login_required
def edit(request, id):
    type_district = TypeDistrict.objects.filter(relation_id=127).order_by('description')
    roles = Rol.objects.all()
    user_edit = User.objects.get(id=id)
    context = {
        'type_district': type_district,
        'roles': roles,
        'user_edit': user_edit
    }
    return render(request, 'user/edit.html', context)


@login_required
def update(request, id):
    roles = Rol.objects.all()
    user_edit = User.objects.get(id=id)

    if request.method == 'POST':
        try:
            user_edit.type_dep = TypeDepartament.objects.get(id=14)
            user_edit.type_prov = TypeProvince.objects.get(id=127)
            user_edit.type_dist = TypeDistrict.objects.get(id=request.POST['type_dist'])
            user_edit.first_name = (request.POST['first_name']).upper().strip()
            user_edit.last_name = (request.POST['last_name']).upper().strip()
            user_edit.phone = request.POST['phone'].strip()
            user_edit.email = request.POST['email'].strip()
            user_edit.full_name_emergency_contact = request.POST['full_name_emergency_contact'].upper().strip()
            user_edit.phone_emergency_contact = request.POST['phone_emergency_contact'].strip()
            # user_edit.set_password(request.POST['password'])
            user_edit.rol = Rol.objects.get(id=request.POST['rol'])
            user_edit.status = request.POST.get('status', False)
            user_edit.status = True if user_edit.status == "on" else False
            user_edit.updated_user = User.objects.get(id=request.user.id).id
            user_edit.save()
            return redirect('/user/')
        except Exception as ex:
            message = 'Email o username ya existe.'
            messages.add_message(request, messages.INFO, message)
            return redirect('/user/')
    else:
        context = {
            'user_edit': user_edit,
            'roles': roles
        }
        return render(request, 'user/edit.html', context)


@login_required
def delete(request, id):
    user = User.objects.get(id=id)
    user.deleted_at = datetime.now()
    user.deleted_user = User.objects.get(id=request.user.id).id
    user.status = False
    user.save()
    return redirect('/user/')


@login_required
def reset_password(request, id):
    user_reset_password = User.objects.get(id=id)
    # Start data for send
    email = user_reset_password.email
    first_name = user_reset_password.first_name
    last_name = user_reset_password.last_name
    # End data for send
    password = generate_password()
    # print(password)
    user_reset_password.set_password(password)
    user_reset_password.save()

    # #Send Email to New Users

    # context = {
    #     'STATIC_ROOT': STATIC_ROOT,
    #     'email': email,
    #     'first_name': first_name,
    #     'last_name': last_name,
    #     'password': password,
    #     'mail_action': 'reset'
    #     }
    # email_subject = 'Bienvenido a la plataforma MiCancha'
    # email_template = 'send_email/send_email_user.html'

    # # Render the template with the provided context
    # email_content = render_to_string(email_template, context)

    # # Create the EmailMessage object
    # email = EmailMessage(
    #     email_subject,
    #     email_content,
    #     settings.EMAIL_HOST_USER,  # Sender's email address
    #     [email],  # Recipient's email address
    # )

    # # Set the content type of the email to HTML
    # email.content_subtype = 'html'

    # # Send the email
    # email.send()

    message = 'Contraseña reseteada correctamente.'
    messages.add_message(request, messages.INFO, message)
    return redirect('/user/')


@login_required
def search(request):
    query = (request.POST['search']).upper()
    users = User.objects.filter(last_name__contains=query)
    context = {
        'users': users
    }
    return render(request, 'user/show.html', context)
