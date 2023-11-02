from django.shortcuts import render, redirect
from appFieldSoccer.models import FieldSoccer
from typeThings.models import TypeFieldSoccer
from appEstablishment.models import Establishment
from modificationHistory.models import HistoryFieldSoccer
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
import base64

def handle_decode_image_base64(image):
    image_decode = image.decode("utf-8")
    return image_decode

@login_required
def create(request):
    type_field_soccers = TypeFieldSoccer.objects.all()
    establishments = Establishment.objects.filter(owner=request.user)

    if request.method == 'POST':
        try:
            if (len(FieldSoccer.objects.filter(name=request.POST['name'].strip(),
                                               establishment=Establishment.objects.get(id=request.POST['establishment']))) == 0):
                field_soccer_create = FieldSoccer()
                field_soccer_create.name = (request.POST['name']).upper().strip()
                field_soccer_create.number_players = (request.POST['number_players']).strip()
                field_soccer_create.price = (request.POST['price']).strip().replace(",", ".")
                field_soccer_create.type_field_soccer = TypeFieldSoccer.objects.get(id=request.POST['type_field_soccer'])
                field_soccer_create.establishment = Establishment.objects.get(id=request.POST['establishment'])
                field_soccer_create.created_user = request.user.id
                field_soccer_create.status = True

                try:
                    ALLOWED_EXTENSIONS_IMAGE = set(['png', 'PNG', 'jpg', 'JPG', 'bmp', 'jpeg', 'JPEG'])
                    image_field_soccer = request.FILES['image']
                    if not (image_field_soccer and image_field_soccer.name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_IMAGE):
                        message = 'Algo salió mal, contacte a TI.'
                        return redirect(f'/field_soccer/', message=message)
                    field_soccer_create.image_base64 = base64.b64encode(image_field_soccer.read())
                except Exception as ex:
                    pass

                field_soccer_create.save()

                history_field_soccer_create = HistoryFieldSoccer()
                history_field_soccer_create.name = (request.POST['name']).upper().strip()
                history_field_soccer_create.number_players = (request.POST['number_players']).strip()
                history_field_soccer_create.price = (request.POST['price']).strip().replace(",", ".")
                history_field_soccer_create.type_field_soccer = TypeFieldSoccer.objects.get(id=request.POST['type_field_soccer'])
                history_field_soccer_create.establishment = Establishment.objects.get(id=request.POST['establishment'])
                history_field_soccer_create.created_at = field_soccer_create.created_at
                history_field_soccer_create.created_user = field_soccer_create.created_user
                history_field_soccer_create.status = True
                history_field_soccer_create.user_session = request.user
                history_field_soccer_create.field_soccer = field_soccer_create

                try:
                    history_field_soccer_create.image_base64 = field_soccer_create.image_base64
                except Exception as ex:
                    pass

                history_field_soccer_create.save()
                return redirect("/field_soccer/")
            else:
                message = 'Campo deportivo ya existe.'
                messages.add_message(request, messages.INFO, message)
                return redirect('/field_soccer/')
        except Exception as ex:
            message = 'Algo salió mal, contacte a TI.'
            messages.add_message(request, messages.INFO, message)
            return redirect('/field_soccer/')
    else:
        context = {
            "type_field_soccers": type_field_soccers,
            "establishments": establishments
        }
        return render(request, 'field_soccer/create.html', context)

@login_required
def show(request):
    images = []
    # Obtener los establecimientos del usuario actual
    if request.user.rol.id == 2:
        establishments = Establishment.objects.filter(owner=request.user.id)
    else:
        establishments = Establishment.objects.all()

    # Filtrar los FieldSoccer que pertenecen a los establecimientos del propietario
    field_soccers = FieldSoccer.objects.filter(establishment__in=establishments).order_by('-created_at')

    for image in field_soccers:
        images.append((image, handle_decode_image_base64(image.image_base64)))

    context = {
        'field_soccers': images
    }
    return render(request, 'field_soccer/show.html', context)


@login_required
def edit(request, id):
    type_field_soccers = TypeFieldSoccer.objects.all()
    establishments = Establishment.objects.filter(owner=request.user)
    field_soccer_edit = FieldSoccer.objects.get(id=id)
    image_base64 = field_soccer_edit.image_base64.decode("utf-8")
    context = {
        'field_soccer_edit': field_soccer_edit,
        "type_field_soccers": type_field_soccers,
        "establishments": establishments,
        'image_base64': image_base64
    }

    return render(request, 'field_soccer/edit.html', context)


@login_required
def update(request, id):
    field_soccer_edit = FieldSoccer.objects.get(id=id)

    if request.method == 'POST':
        try:
            field_soccer_edit.name = (request.POST['name']).upper().strip()
            field_soccer_edit.number_players = (request.POST['number_players']).strip()
            field_soccer_edit.price = (request.POST['price']).strip().replace(",", ".")
            field_soccer_edit.type_field_soccer = TypeFieldSoccer.objects.get(id=request.POST['type_field_soccer'])
            field_soccer_edit.establishment = Establishment.objects.get(id=request.POST['establishment'])
            field_soccer_edit.updated_at = datetime.now()
            field_soccer_edit.updated_user = request.user.id
            field_soccer_edit.status = request.POST.get('status', False)
            field_soccer_edit.status = True if field_soccer_edit.status == "on" else False

            try:
                ALLOWED_EXTENSIONS_IMAGE = set(['png', 'PNG', 'jpg', 'JPG', 'bmp', 'jpeg', 'JPEG'])
                image_field_soccer = request.FILES['image']
                if not (image_field_soccer and image_field_soccer.name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_IMAGE):
                    message = 'Algo salió mal, contacte a TI.'
                    return redirect(f'/field_soccer/', message=message)
                field_soccer_edit.image_base64 = base64.b64encode(image_field_soccer.read())
            except Exception as ex:
                pass

            field_soccer_edit.save()

            history_field_soccer_edit = HistoryFieldSoccer()
            history_field_soccer_edit.name = (request.POST['name']).upper().strip()
            history_field_soccer_edit.number_players = (request.POST['number_players']).strip()
            history_field_soccer_edit.price = (request.POST['price']).strip().replace(",", ".")
            history_field_soccer_edit.type_field_soccer = TypeFieldSoccer.objects.get(id=request.POST['type_field_soccer'])
            history_field_soccer_edit.establishment = Establishment.objects.get(id=request.POST['establishment'])
            history_field_soccer_edit.created_at = field_soccer_edit.created_at
            history_field_soccer_edit.created_user = field_soccer_edit.created_user
            history_field_soccer_edit.updated_at = field_soccer_edit.updated_at
            history_field_soccer_edit.updated_user = field_soccer_edit.updated_user
            history_field_soccer_edit.status = True
            history_field_soccer_edit.user_session = request.user
            history_field_soccer_edit.field_soccer = FieldSoccer.objects.get(id=id)

            try:
                history_field_soccer_edit.image_base64 = field_soccer_edit.image_base64
            except Exception as ex:
                pass

            history_field_soccer_edit.save()
            return redirect("/field_soccer/")
        except Exception as ex:
            print(ex)
            message = 'Algo salió mal, contacte a TI.'
            messages.add_message(request, messages.INFO, message)
            return redirect('/field_soccer/')
    else:
        context = {
            'field_soccer_edit': field_soccer_edit,
        }
        return render(request, 'field_soccer/edit.html', context)


@login_required
def delete(request, id):
    field_soccer_delete = FieldSoccer.objects.get(id=id)
    field_soccer_delete.deleted_at = datetime.now()
    field_soccer_delete.deleted_user = request.user.id
    field_soccer_delete.status = False
    field_soccer_delete.save()

    history_field_soccer_delete = HistoryFieldSoccer()
    history_field_soccer_delete.name = field_soccer_delete.name
    history_field_soccer_delete.number_players = field_soccer_delete.number_players
    history_field_soccer_delete.price = field_soccer_delete.price
    history_field_soccer_delete.type_field_soccer = field_soccer_delete.type_field_soccer
    history_field_soccer_delete.establishment = field_soccer_delete.establishment
    history_field_soccer_delete.created_at = field_soccer_delete.created_at
    history_field_soccer_delete.created_user = field_soccer_delete.created_user
    history_field_soccer_delete.updated_at = field_soccer_delete.updated_at
    history_field_soccer_delete.updated_user = field_soccer_delete.updated_user
    history_field_soccer_delete.deleted_at = datetime.now()
    history_field_soccer_delete.deleted_user = request.user.id
    history_field_soccer_delete.status = False
    history_field_soccer_delete.user_session = request.user
    history_field_soccer_delete.field_soccer = FieldSoccer.objects.get(id=id)
    history_field_soccer_delete.save()
    return redirect('/field_soccer/')

@login_required
def historial(request, id):
    images = []

    historial_field_soccers = HistoryFieldSoccer.objects.filter(field_soccer=id).order_by('-updated_at')

    for image in historial_field_soccers:
        if image.image_base64 != None:
            images.append((image, handle_decode_image_base64(image.image_base64)))
        else:
            images.append((image, None))

    context = {
        'historial_field_soccers': images
    }    

    return render(request, 'field_soccer/historial.html', context)