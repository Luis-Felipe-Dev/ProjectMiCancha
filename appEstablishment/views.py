from django.shortcuts import render, redirect
from appEstablishment.models import Establishment
from typeThings.models import TypeDepartament, TypeProvince, TypeDistrict
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def create(request):
    type_district = TypeDistrict.objects.filter(relation_id=127)
    
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
                establishment_create.created_at = datetime.now()
                establishment_create.created_user = request.user.id
                establishment_create.status = True
                establishment_create.save()
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
    establishments = Establishment.objects.all()
    context = {
        'establishments': establishments
    }
    return render(request, 'establishment/show.html', context)


@login_required
def edit(request, id):
    establishment_edit = Establishment.objects.get(id=id)
    type_district = TypeDistrict.objects.filter(relation_id=127)
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
            if (len(Establishment.objects.filter(name=request.POST['name'].strip(),
                                                    type_dist=TypeDistrict.objects.get(id=request.POST['type_dist']))) == 0):
                establishment_edit.name = (request.POST['name']).upper().strip()
                establishment_edit.location = (request.POST['location']).upper().strip()
                establishment_edit.phone = request.POST['phone'].strip()
                establishment_edit.type_dep = TypeDepartament.objects.get(id=14)
                establishment_edit.type_prov = TypeProvince.objects.get(id=127)
                establishment_edit.type_dist = TypeDistrict.objects.get(id=request.POST['type_dist'])
                establishment_edit.updated_at = datetime.now()
                establishment_edit.updated_user = request.user.id
                establishment_edit.status = request.POST.get('status', False)
                establishment_edit.status = True if establishment_edit.status == "on" else False
                establishment_edit.save()
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
    return redirect('/establishment/')