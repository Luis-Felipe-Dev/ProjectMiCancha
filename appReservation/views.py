from django.shortcuts import render, redirect
from appReservation.models import Reservation
from appFieldSoccer.models import FieldSoccer
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def create(request):
    field_soccers = FieldSoccer.objects.all()

    if request.method == 'POST':
        try:
            reservation_create = Reservation()
            reservation_create.date = request.POST['date']
            reservation_create.start_hour = request.POST['start_hour']
            reservation_create.end_hour = request.POST['end_hour']
            reservation_create.field_soccer = request.POST['field_soccer']
            reservation_create.customer = request.user.id
            reservation_create.created_at = datetime.now()
            reservation_create.created_user = request.user.id
            reservation_create.status = True
            reservation_create.save()
            return redirect("/reservation/")
        except ValidationError as e:
            message = 'Algo salió mal, contacte a TI.'
            return redirect('/reservation/', message=message)
    else:
        context = {
            "field_soccers": field_soccers
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