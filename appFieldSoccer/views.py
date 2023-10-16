from django.shortcuts import render, redirect
from appFieldSoccer.models import FieldSoccer
from typeThings.models import TypeFieldSoccer
from appEstablishment.models import Establishment
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def create(request):
    type_field_soccers = TypeFieldSoccer.objects.all()
    establishments = Establishment.objects.all()

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
                field_soccer_create.created_at = datetime.now()
                field_soccer_create.created_user = request.user.id
                field_soccer_create.status = True
                field_soccer_create.save()
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
    field_soccers = FieldSoccer.objects.all()
    context = {
        'field_soccers': field_soccers
    }
    return render(request, 'field_soccer/show.html', context)


@login_required
def edit(request, id):
    type_field_soccers = TypeFieldSoccer.objects.all()
    establishments = Establishment.objects.all()
    field_soccer_edit = FieldSoccer.objects.get(id=id)
    context = {
        'field_soccer_edit': field_soccer_edit,
        "type_field_soccers": type_field_soccers,
        "establishments": establishments
    }

    return render(request, 'field_soccer/edit.html', context)


@login_required
def update(request, id):
    field_soccer_edit = FieldSoccer.objects.get(id=id)

    if request.method == 'POST':
        try:
            # if (len(FieldSoccer.objects.filter(name=request.POST['name'].strip().upper(),
            #                        establishment=Establishment.objects.get(id=request.POST['establishment']))) == 0):
            #     field_soccer_edit.name = (request.POST['name']).upper().strip()
            #     field_soccer_edit.number_players = (request.POST['number_players']).strip()
            #     field_soccer_edit.price = (request.POST['price']).strip().replace(",", ".")
            #     field_soccer_edit.type_field_soccer = TypeFieldSoccer.objects.get(id=request.POST['type_field_soccer'])
            #     field_soccer_edit.establishment = Establishment.objects.get(id=request.POST['establishment'])
            #     field_soccer_edit.updated_at = datetime.now()
            #     field_soccer_edit.updated_user = request.user.id
            #     field_soccer_edit.status = request.POST.get('status', False)
            #     field_soccer_edit.status = True if field_soccer_edit.status == "on" else False
            #     field_soccer_edit.save()
            #     return redirect("/field_soccer/")
            # else:
            #     message = 'Campo deportivo ya existe.'
            #     messages.add_message(request, messages.INFO, message)
            #     return redirect('/field_soccer/')
            field_soccer_edit.name = (request.POST['name']).upper().strip()
            field_soccer_edit.number_players = (request.POST['number_players']).strip()
            field_soccer_edit.price = (request.POST['price']).strip().replace(",", ".")
            field_soccer_edit.type_field_soccer = TypeFieldSoccer.objects.get(id=request.POST['type_field_soccer'])
            field_soccer_edit.establishment = Establishment.objects.get(id=request.POST['establishment'])
            field_soccer_edit.updated_at = datetime.now()
            field_soccer_edit.updated_user = request.user.id
            field_soccer_edit.status = request.POST.get('status', False)
            field_soccer_edit.status = True if field_soccer_edit.status == "on" else False
            field_soccer_edit.save()
            return redirect("/field_soccer/")
        except Exception as ex:
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
    return redirect('/field_soccer/')