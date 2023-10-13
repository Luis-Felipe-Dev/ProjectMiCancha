from django.shortcuts import render, redirect
from appReservation.models import Reservation
from appFieldSoccer.models import FieldSoccer
from appUser.models import User
from typeThings.models import TypeDistrict
from appEstablishment.models import Establishment
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse

@login_required
def create(request):
    type_district = TypeDistrict.objects.filter(relation_id=127)
    establishments = Establishment.objects.all()
    field_soccers = FieldSoccer.objects.all()

    if request.method == 'POST':
        try:
            # Capturar horas seleccionadas del campo oculto
            horas_seleccionadas = request.POST.get('horas_seleccionadas', '')
            horas = horas_seleccionadas.split(',')
            print(horas_seleccionadas)
            # horas_seleccionadas = request.POST.get('horas_seleccionadas')

            # # Dividir las horas seleccionadas en hora de inicio y hora de fin
            # hora_inicio, hora_fin = horas_seleccionadas.split('-')

            reservation_create = Reservation()
            reservation_create.date = request.POST['date']
            # reservation_create.start_hour = request.POST['start_hour']
            # reservation_create.end_hour = request.POST['end_hour']
            reservation_create.start_hour = horas[0].strip()
            reservation_create.end_hour = horas[1].strip()

            reservation_create.field_soccer = FieldSoccer.objects.get(id=request.POST['field_soccer'])
            reservation_create.customer = User.objects.get(id=request.user.id)
            reservation_create.created_at = datetime.now()
            reservation_create.created_user = request.user.id
            reservation_create.status = True
            print(reservation_create.date)
            # print(request.POST['start_hour'])
            # print(request.POST['end_hour'])
            print(reservation_create.start_hour)
            print(reservation_create.end_hour)
            print(reservation_create.field_soccer)
            print(reservation_create.customer)
            print(reservation_create.created_at)
            # reservation_create.save()
            return redirect("/reservation/")
        except ValidationError as e:
            message = 'Algo salió mal, contacte a TI.'
            return redirect('/reservation/', message=message)
    else:
        context = {
            'type_district': type_district,
            'establishments': establishments,
            'field_soccers': field_soccers
        }
        return render(request, 'reservation/create.html', context)


@login_required
def show(request):
    reservations = Reservation.objects.all()
    context = {
        'reservations': reservations
    }
    return render(request, 'reservation/show.html', context)


@login_required
def edit(request, id):
    reservation_edit = Reservation.objects.get(id=id)
    context = {
        'reservation_edit': reservation_edit
    }

    return render(request, 'reservation/edit.html', context)


@login_required
def update(request, id):
    reservation_edit = FieldSoccer.objects.get(id=id)

    if request.method == 'POST':
        try:
            reservation_edit.date = request.POST['date']
            reservation_edit.start_hour = request.POST['start_hour']
            reservation_edit.end_hour = request.POST['end_hour']
            reservation_edit.field_soccer = request.POST['field_soccer']
            reservation_edit.customer = request.user.id
            reservation_edit.created_at = datetime.now()
            reservation_edit.created_user = request.user.id
            reservation_edit.status = request.POST.get('status', False)
            reservation_edit.status = True if reservation_edit.status == "on" else False
            reservation_edit.save()
            return redirect("/reservation/")
        except ValidationError as e:
            message = 'Algo salió mal, contacte a TI.'
            return redirect('/reservation/', message=message)
    else:
        context = {
            'reservation_edit': reservation_edit,
        }
        return render(request, 'reservation/edit.html', context)


@login_required
def delete(request, id):
    reservation_delete = Reservation.objects.get(id=id)
    reservation_delete.deleted_at = datetime.now()
    reservation_delete.deleted_user = request.user.id
    reservation_delete.status = False
    reservation_delete.save()
    return redirect('/reservation/')

def get_establishment(request, type_dist_id):
    establishments = Establishment.objects.filter(type_dist=type_dist_id).values('id', 'name')
    print(establishments)
    return JsonResponse({'establishments': list(establishments)})

def get_field_soccer(request, establishment_id):
    field_soccer = FieldSoccer.objects.filter(establishment=establishment_id).values('id', 'name')
    print(field_soccer)
    return JsonResponse({'field_soccer': list(field_soccer)})