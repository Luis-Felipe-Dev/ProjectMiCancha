from django.shortcuts import render, redirect
from appEstablishment.models import Establishment
from modificationHistory.models import HistoryEstablishment
from typeThings.models import TypeDepartament, TypeProvince, TypeDistrict
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def create(request):
    type_district = TypeDistrict.objects.filter(relation_id=127).order_by('description')
    
    if request.method == 'POST':
        try:
            if (len(Establishment.objects.filter(name=request.POST['name'].strip(),
                                                 type_dist=TypeDistrict.objects.get(id=request.POST['type_dist']))) == 0):
                establishment_create = Establishment()
                establishment_create.name = (request.POST['name']).upper().strip()
                establishment_create.location = (request.POST['location']).upper().strip()
                establishment_create.phone = request.POST['phone'].strip()
                establishment_create.type_dep = TypeDepartament.objects.get(id=14)
                establishment_create.type_prov = TypeProvince.objects.get(id=127)
                establishment_create.type_dist = TypeDistrict.objects.get(id=request.POST['type_dist'])
                establishment_create.created_user = request.user.id
                establishment_create.owner = request.user
                establishment_create.latitude = request.POST['latitude'].replace(',', '.')
                establishment_create.longitude = request.POST['longitude'].replace(',', '.')
                establishment_create.status = True
                establishment_create.save()

                history_establishment_create = HistoryEstablishment()
                history_establishment_create.name = (request.POST['name']).upper().strip()
                history_establishment_create.location = (request.POST['location']).upper().strip()
                history_establishment_create.phone = request.POST['phone'].strip()
                history_establishment_create.type_dep = TypeDepartament.objects.get(id=14)
                history_establishment_create.type_prov = TypeProvince.objects.get(id=127)
                history_establishment_create.type_dist = TypeDistrict.objects.get(id=request.POST['type_dist'])
                history_establishment_create.created_at = establishment_create.created_at
                history_establishment_create.created_user = establishment_create.created_user
                history_establishment_create.owner = request.user
                history_establishment_create.latitude = establishment_create.latitude
                history_establishment_create.longitude = establishment_create.latitude
                history_establishment_create.status = True
                history_establishment_create.user_session = request.user
                history_establishment_create.establishment = establishment_create
                history_establishment_create.save()
                return redirect("/establishment/")
            else:
                message = 'Establecimiento ya existe.'
                messages.add_message(request, messages.INFO, message)
                return redirect('/establishment/')
        except Exception as ex:
            message = 'Algo salió mal, contacte a TI.'
            messages.add_message(request, messages.INFO, message)
            return redirect('/establishment/')
    else:
        context = {
            'type_district': type_district
        }
        return render(request, 'establishment/create.html', context)


@login_required
def show(request):
    establishments = Establishment.objects.filter(owner=request.user.id).order_by('-created_at')\
                    if request.user.rol.id == 2 else Establishment.objects.all().order_by('-created_at')
    context = {
        'establishments': establishments
    }
    return render(request, 'establishment/show.html', context)


@login_required
def edit(request, id):
    establishment_edit = Establishment.objects.get(id=id)
    type_district = TypeDistrict.objects.filter(relation_id=127).order_by('description')
    context = {
        'establishment_edit': establishment_edit,
        'type_district': type_district
    }
    return render(request, 'establishment/edit.html', context)


@login_required
def update(request, id):
    establishment_edit = Establishment.objects.get(id=id)

    if request.method == 'POST':
        try:
            establishment_edit.name = (request.POST['name']).upper().strip()
            establishment_edit.location = (request.POST['location']).upper().strip()
            establishment_edit.phone = request.POST['phone'].strip()
            establishment_edit.type_dep = TypeDepartament.objects.get(id=14)
            establishment_edit.type_prov = TypeProvince.objects.get(id=127)
            establishment_edit.type_dist = TypeDistrict.objects.get(id=request.POST['type_dist'])
            establishment_edit.updated_at = datetime.now()
            establishment_edit.updated_user = request.user.id
            establishment_edit.owner = request.user
            establishment_edit.latitude = request.POST['latitude'].replace(',', '.')
            establishment_edit.longitude = request.POST['longitude'].replace(',', '.')
            establishment_edit.status = request.POST.get('status', False)
            establishment_edit.status = True if establishment_edit.status == "on" else False
            establishment_edit.save()

            history_establishment_edit = HistoryEstablishment()
            history_establishment_edit.name = (request.POST['name']).upper().strip()
            history_establishment_edit.location = (request.POST['location']).upper().strip()
            history_establishment_edit.phone = request.POST['phone'].strip()
            history_establishment_edit.type_dep = TypeDepartament.objects.get(id=14)
            history_establishment_edit.type_prov = TypeProvince.objects.get(id=127)
            history_establishment_edit.type_dist = TypeDistrict.objects.get(id=request.POST['type_dist'])
            history_establishment_edit.created_at = establishment_edit.created_at
            history_establishment_edit.created_user = establishment_edit.created_user
            history_establishment_edit.updated_at = establishment_edit.created_at
            history_establishment_edit.updated_user = establishment_edit.updated_user
            history_establishment_edit.owner = establishment_edit.owner
            history_establishment_edit.latitude = establishment_edit.latitude
            history_establishment_edit.longitude = establishment_edit.longitude
            history_establishment_edit.status = True
            history_establishment_edit.user_session = request.user
            history_establishment_edit.establishment = Establishment.objects.get(id=id)
            history_establishment_edit.save()
            return redirect('/establishment/')
        except Exception as ex:
            print(ex)
            message = 'Algo salió mal, contacte a TI.'
            messages.add_message(request, messages.INFO, message)
            return redirect('/establishment/')
    else:
        context = {
            'establishment_edit': establishment_edit,
        }
        return render(request, 'establishment/edit.html', context)


@login_required
def delete(request, id):
    establishment_delete = Establishment.objects.get(id=id)
    establishment_delete.deleted_at = datetime.now()
    establishment_delete.deleted_user = request.user.id
    establishment_delete.status = False
    establishment_delete.save()

    history_establishment_delete = HistoryEstablishment()
    history_establishment_delete.name = establishment_delete.name
    history_establishment_delete.location = establishment_delete.location
    history_establishment_delete.phone = establishment_delete.phone
    history_establishment_delete.type_dep = establishment_delete.type_dep
    history_establishment_delete.type_prov = establishment_delete.type_prov
    history_establishment_delete.type_dist = establishment_delete.type_dist
    history_establishment_delete.created_at = establishment_delete.created_at
    history_establishment_delete.created_user = establishment_delete.created_user
    history_establishment_delete.updated_at = establishment_delete.updated_at
    history_establishment_delete.updated_user = establishment_delete.updated_user
    history_establishment_delete.deleted_at = datetime.now()
    history_establishment_delete.deleted_user = request.user.id
    history_establishment_delete.owner = establishment_delete.owner
    history_establishment_delete.latitude = establishment_delete.latitude
    history_establishment_delete.longitude = establishment_delete.longitude
    history_establishment_delete.status = False
    history_establishment_delete.user_session = request.user
    history_establishment_delete.establishment = Establishment.objects.get(id=id)
    history_establishment_delete.save()
    return redirect('/establishment/')

@login_required
def historial(request, id):
    historial_establishments = HistoryEstablishment.objects.filter(establishment=id).order_by('-updated_at')
    context = {
        'historial_establishments': historial_establishments
    }
    return render(request, 'establishment/historial.html', context)