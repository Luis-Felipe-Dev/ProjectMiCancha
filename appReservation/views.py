from django.shortcuts import render, redirect
from appReservation.models import Reservation
from appFieldSoccer.models import FieldSoccer
from appUser.models import User
from typeThings.models import TypeDistrict
from appEstablishment.models import Establishment
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, time
from django.http import JsonResponse

@login_required
def create(request):
    type_district = TypeDistrict.objects.filter(relation_id=127)
    establishments = Establishment.objects.all()
    field_soccers = FieldSoccer.objects.all()

    if request.method == 'POST':
        try:
            selected_hours = request.POST.getlist('option_hour')

            if selected_hours:
                selected_hours.sort()
                consecutive_hours = True
                for i in range(1, len(selected_hours)):
                    current_hour = datetime.strptime(selected_hours[i], '%H:%M')
                    previous_hour = datetime.strptime(selected_hours[i - 1], '%H:%M')

                    # Comprueba si la hora actual es consecutiva con la anterior
                    if current_hour != previous_hour + timedelta(hours=1):
                        consecutive_hours = False
                        break
                if consecutive_hours:
                    reservation_create = Reservation()
                    reservation_create.date = request.POST['date_reservation']
                    reservation_create.start_hour = selected_hours[0].strip()
                    reservation_create.end_hour = (datetime.strptime(selected_hours[-1].strip(), '%H:%M') + timedelta(hours=1)).strftime('%H:%M')
                    reservation_create.field_soccer = FieldSoccer.objects.get(id=request.POST['field_soccer'])
                    reservation_create.customer = User.objects.get(id=request.user.id)
                    reservation_create.created_at = datetime.now()
                    reservation_create.created_user = request.user.id
                    reservation_create.status = True
                    reservation_create.save()
                    print("Reserva guardada con éxito.")
                else:
                    print("Las horas seleccionadas no son consecutivas. Por favor, seleccione horas consecutivas para la reserva.")
            else:
                print("No selecionó una hora de reserva.")
            return redirect("/reservation/")
        except ValidationError as e:
            print(e)
            message = f'Algo salió mal, contacte a TI. {e}'
            return redirect('/reservation/', message=message)
        except Exception as e:
            print(e)
            message = f'Algo salió mal, contacte a TI. {e}'
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

# @method_decorator(csrf_exempt)
def get_establishment(request, type_dist_id):
    establishments = Establishment.objects.filter(type_dist=type_dist_id).values("id", "name")
    return JsonResponse({'establishments': list(establishments)})

# @method_decorator(csrf_exempt)
def get_field_soccer(request, establishment_id):
    field_soccer = FieldSoccer.objects.filter(establishment=establishment_id).values('id', 'name')
    return JsonResponse({'field_soccer': list(field_soccer)})

# @method_decorator(csrf_exempt)
def get_reservation(request, field_soccer_id, date_reservation):
    reservations = Reservation.objects.filter(field_soccer=field_soccer_id, date=date_reservation).values('id', 'start_hour', 'end_hour')
    return JsonResponse({'reservations': list(reservations)})

def get_available_hours(request, field_soccer_id, date_reservation):
    # Parsea la fecha de la solicitud
    requested_date = datetime.strptime(date_reservation, '%Y-%m-%d').date()

    # Obtén todas las reservas para el campo de fútbol y la fecha solicitados
    reservations = Reservation.objects.filter(field_soccer=field_soccer_id, date=requested_date)

    # Crea una lista de horas disponibles inicialmente con todas las horas del día
    available_hours = [f'{hour:02}:00' for hour in range(0, 24)]

    # Elimina las horas que están reservadas
    for reservation in reservations:
        start_hour = int(reservation.start_hour.strftime('%H'))
        end_hour = int(reservation.end_hour.strftime('%H'))

        # Elimina las horas reservadas del rango de horas disponibles
        available_hours = [hour for hour in available_hours if not (start_hour <= int(hour[:2]) < end_hour)]

        print(available_hours)

    # Devuelve las horas disponibles como una lista en la respuesta JSON
    return JsonResponse({'available_hours': available_hours})