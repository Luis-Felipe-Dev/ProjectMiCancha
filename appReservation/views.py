from django.shortcuts import render, redirect, get_object_or_404
from appReservation.models import Reservation
from appFieldSoccer.models import FieldSoccer
from appFieldSoccer.views import handle_decode_image_base64
from appUser.models import User
from typeThings.models import TypeDistrict, TypeStatus
from appEstablishment.models import Establishment
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

@login_required
def create(request):
    now_filter = datetime.now().strftime('%H')
    type_district = TypeDistrict.objects.filter(relation_id=127).order_by('description')
    establishments = Establishment.objects.all()
    field_soccers = FieldSoccer.objects.all()

    if request.method == 'POST':
        try:
            selected_hours = request.POST.getlist('option_hour')
            # print(selected_hours)

            if selected_hours:
                reservations_to_create = []

                # Crear una reserva para cada hora seleccionada
                for hour in selected_hours:
                    start_hour = hour.strip()
                    end_hour = (datetime.strptime(start_hour, '%H:%M') + timedelta(hours=1)).strftime('%H:%M')
                    reservation = Reservation(
                        date=request.POST['date_reservation'],
                        start_hour=start_hour,
                        end_hour=end_hour,
                        field_soccer=FieldSoccer.objects.get(id=request.POST['field_soccer']),
                        customer=User.objects.get(id=request.user.id),
                        created_at=datetime.now(),
                        created_user=request.user.id,
                        type_status=TypeStatus.objects.get(id=1),
                    )
                    reservations_to_create.append(reservation)

                # Guardar las reservas
                for reservation in reservations_to_create:
                    #Send Email to customers
                    email = request.user

                    context = {
                        'email': email,
                        'date': reservation.date,
                        'start_hour': reservation.start_hour,
                        'end_hour': reservation.end_hour,
                        'field_soccer_name': reservation.field_soccer.name,
                        'field_soccer_number_players': reservation.field_soccer.number_players,
                        'field_soccer_price': reservation.field_soccer.price,
                        'field_soccer_image_base64': reservation.field_soccer.image_base64.decode("utf-8"),
                        'establishment_name': reservation.field_soccer.establishment.name,
                        'establishment_location': reservation.field_soccer.establishment.location,
                        'establishment_phone': reservation.field_soccer.establishment.phone,
                        'establishment_type_dist': reservation.field_soccer.establishment.type_dist.complete
                        }
                    
                    # # Send Email
                    # email_subject = f'MiCancha - Reserva de campo deportivo para el {reservation.date} de {reservation.start_hour} a {reservation.end_hour}'
                    # email_template = 'send_email/reservation.html'
                    # email_content = render_to_string(email_template, context)
                    # email = EmailMessage(
                    #     email_subject,
                    #     email_content,
                    #     settings.EMAIL_HOST_USER,
                    #     ['luis.fhb.2016@gmail.com'],
                    # )
                    # email.content_subtype = 'html'
                    # email.send()

                    reservation.save()
                print("Reservas guardadas con éxito.")
            else:
                print("No seleccionó ninguna hora de reserva.")
            return redirect("/reservation/")
        except Exception as e:
            print(e)
            message = f'Algo salió mal, contacte a TI. {e}'
            return redirect('/reservation/', message=message)
    else:
        context = {
            'type_district': type_district,
            'establishments': establishments,
            'field_soccers': field_soccers,
            'now_filter': int(now_filter)
        }
        return render(request, 'reservation/create.html', context)

@login_required
def show(request):
    for reservation in Reservation.objects.filter(type_status=1):
        # Obtener la diferencia de tiempo entre la fecha de creación y el tiempo actual
        time_difference = timezone.now() - reservation.created_at

        # Verificar si han pasado exactamente 30 minutos
        if time_difference >= timedelta(minutes=30):
            # Actualizar el estado a TypeStatus con ID 3
            reservation.type_status = TypeStatus.objects.get(id=3)
            reservation.save()
        else:
            pass

    if request.user.rol.id == 3:
        reservations = Reservation.objects.filter(created_user=request.user.id).order_by('-created_at')
    
    elif request.user.rol.id == 2:
        field_soccers = FieldSoccer.objects.filter(establishment__owner=request.user)
        reservations = Reservation.objects.filter(field_soccer__in=field_soccers).order_by('-created_at')
    
    else:
        # Si el usuario tiene otro rol, muestra todas las reservaciones
        reservations = Reservation.objects.all().order_by('-created_at')
    
    for field in reservations:
        field.field_soccer.establishment.latitude = str(field.field_soccer.establishment.latitude).replace(',', '.')
        field.field_soccer.establishment.longitude = str(field.field_soccer.establishment.longitude).replace(',', '.')

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
    reservation_edit = Reservation.objects.get(id=id)

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
    print(id)
    try:
        reservation_delete = Reservation.objects.get(id=id)
        reservation_delete.deleted_at = datetime.now()
        reservation_delete.deleted_user = request.user.id
        reservation_delete.type_status = TypeStatus.objects.get(id=3)
        reservation_delete.save()
                
        email = request.user
        context = {
            'email': email,
            'date': reservation_delete.date,
            'start_hour': reservation_delete.start_hour,
            'end_hour': reservation_delete.end_hour,
            'field_soccer_name': reservation_delete.field_soccer.name,
            'field_soccer_number_players': reservation_delete.field_soccer.number_players,
            'field_soccer_price': reservation_delete.field_soccer.price,
            'field_soccer_image_base64': reservation_delete.field_soccer.image_base64.decode("utf-8"),
            'establishment_name': reservation_delete.field_soccer.establishment.name,
            'establishment_location': reservation_delete.field_soccer.establishment.location,
            'establishment_phone': reservation_delete.field_soccer.establishment.phone,
            'establishment_type_dist': reservation_delete.field_soccer.establishment.type_dist.complete,
            'latitude': str(reservation_delete.field_soccer.establishment.latitude).replace(',', '.'),
            'longitude': str(reservation_delete.field_soccer.establishment.longitude).replace(',', '.'),
            'anulada': True
            }
        
        # Send Email
        email_subject = f'MiCancha - Reserva Anulada'
        email_template = 'send_email/reservation.html'
        email_content = render_to_string(email_template, context)
        email = EmailMessage(
            email_subject,
            email_content,
            settings.EMAIL_HOST_USER,
            ['luis.fhb.2016@gmail.com'],
        )
        email.content_subtype = 'html'
        email.send()

    except Exception as ex:
        print(ex)
    return redirect('/reservation/')

# @method_decorator(csrf_exempt)
def get_establishment(request, type_dist_id):
    establishments = Establishment.objects.filter(type_dist=type_dist_id).values("id", "name", "location", "phone")
    return JsonResponse({'establishments': list(establishments)})

# @method_decorator(csrf_exempt)
def get_field_soccer(request, establishment_id):
    field_soccer = FieldSoccer.objects.filter(establishment=establishment_id).values('id', 'name', 'number_players')
    return JsonResponse({'field_soccer': list(field_soccer)})

# # @method_decorator(csrf_exempt)
# def get_reservation(request, field_soccer_id, date_reservation):
#     reservations = Reservation.objects.filter(field_soccer=field_soccer_id, date=date_reservation).values('id', 'start_hour', 'end_hour')
#     return JsonResponse({'reservations': list(reservations)})

def get_available_hours(request, field_soccer_id, date_reservation):
    # Parsea la fecha de la solicitud
    requested_date = datetime.strptime(date_reservation, '%Y-%m-%d').date()

    # Obtén todas las reservas para el campo de fútbol y la fecha solicitados
    reservations = Reservation.objects.filter(field_soccer=field_soccer_id, date=requested_date, type_status=2)

    # Crea una lista de horas disponibles inicialmente con todas las horas del día
    available_hours = [f'{hour:02}:00' for hour in range(9, 24)]

    # Elimina las horas que están reservadas
    unavailable_hours = []
    for reservation in reservations:
        start_hour = int(reservation.start_hour.strftime('%H'))
        end_hour = int(reservation.end_hour.strftime('%H'))

        # Elimina las horas reservadas del rango de horas disponibles
        available_hours = [hour for hour in available_hours if not (start_hour <= int(hour[:2]) < end_hour)]

        # Agrega las horas reservadas a la lista de horas no disponibles
        for hour in range(start_hour, end_hour):
            unavailable_hours.append(f'{hour:02}:00')
    
    context = {
        'available_hours': available_hours,
        'unavailable_hours': unavailable_hours
    }

    # Devuelve las horas disponibles y no disponibles como listas en la respuesta JSON
    return JsonResponse(context)

def get_field_soccer_number_players(request, number_players):
    try:
        field_soccer = []
        field_soccer_objects = FieldSoccer.objects.filter(number_players=number_players)
        for obj in field_soccer_objects:
            decoded_image = handle_decode_image_base64(obj.image_base64)
            field_soccer.append({
                'id': obj.id,
                'name': obj.name,
                'number_players': obj.number_players,
                'price': obj.price,
                'image_base64': decoded_image,
                'establishment': obj.establishment.name,
                'location': obj.establishment.location,
                'phone': obj.establishment.phone,
                'latitude': obj.establishment.latitude,
                'longitude': obj.establishment.longitude,
                'type_field_soccer': obj.type_field_soccer.description
            })
        
        for field in field_soccer_objects:
            field.establishment.latitude = str(field.establishment.latitude).replace(',', '.')
            field.establishment.longitude = str(field.establishment.longitude).replace(',', '.')

        if len(field_soccer) > 0:
            return JsonResponse({'field_soccer': field_soccer})
        else:
            return JsonResponse({'error': 'No se encontraron campos deportivos para el número de jugadores especificado.'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'El número de jugadores especificado no es válido.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required
def select_field_soccer(request, id):
    field_soccer_selected = FieldSoccer.objects.get(id=id)
    image_base64 = field_soccer_selected.image_base64.decode("utf-8")
    context = {
        'field_soccer_selected': field_soccer_selected,
        'image_base64': image_base64
    }

    return render(request, 'field_soccer/select_field_soccer.html', context)

@login_required
def create_select_reservation(request, id):
    now_filter = datetime.now().strftime('%H')
    type_district = TypeDistrict.objects.filter(relation_id=127).order_by('description')
    establishments = Establishment.objects.all()
    field_soccers = FieldSoccer.objects.all()
    field_soccer_selected = FieldSoccer.objects.get(id=id)
    image_base64 = field_soccer_selected.image_base64.decode("utf-8")

    if request.method == 'POST':

        try:
            selected_hours = request.POST.getlist('option_hour')
            # print(selected_hours)

            if selected_hours:
                reservations_to_create = []

                # Crear una reserva para cada hora seleccionada
                for hour in selected_hours:
                    start_hour = hour.strip()
                    end_hour = (datetime.strptime(start_hour, '%H:%M') + timedelta(hours=1)).strftime('%H:%M')
                    reservation = Reservation(
                        date=request.POST['date_reservation'],
                        start_hour=start_hour,
                        end_hour=end_hour,
                        field_soccer=field_soccer_selected,
                        customer=User.objects.get(id=request.user.id),
                        created_at=datetime.now(),
                        created_user=request.user.id,
                        type_status=TypeStatus.objects.get(id=1)
                    )
                    reservations_to_create.append(reservation)

                # Guardar las reservas
                for reservation in reservations_to_create:
                    #Send Email to customers
                    email = request.user

                    context = {
                        'email': email,
                        'date': reservation.date,
                        'start_hour': reservation.start_hour,
                        'end_hour': reservation.end_hour,
                        'field_soccer_name': reservation.field_soccer.name,
                        'field_soccer_number_players': reservation.field_soccer.number_players,
                        'field_soccer_price': reservation.field_soccer.price,
                        'field_soccer_image_base64': reservation.field_soccer.image_base64.decode("utf-8"),
                        'establishment_name': reservation.field_soccer.establishment.name,
                        'establishment_location': reservation.field_soccer.establishment.location,
                        'establishment_phone': reservation.field_soccer.establishment.phone,
                        'establishment_type_dist': reservation.field_soccer.establishment.type_dist.complete
                        }
                    
                    # # Send Email
                    # email_subject = f'MiCancha - Reserva de campo deportivo para el {reservation.date} de {reservation.start_hour} a {reservation.end_hour}'
                    # email_template = 'send_email/reservation.html'
                    # email_content = render_to_string(email_template, context)
                    # email = EmailMessage(
                    #     email_subject,
                    #     email_content,
                    #     settings.EMAIL_HOST_USER,
                    #     ['luis.fhb.2016@gmail.com'],
                    # )
                    # email.content_subtype = 'html'
                    # email.send()

                    reservation.save()
                print("Reservas guardadas con éxito.")
            else:
                print("No seleccionó ninguna hora de reserva.")
            return redirect("/reservation/")
        except Exception as e:
            print(e)
            message = f'Algo salió mal, contacte a TI. {e}'
            return redirect('/reservation/', message=message)
    else:
        context = {
            'type_district': type_district,
            'establishments': establishments,
            'field_soccers': field_soccers,
            'now_filter': int(now_filter),
            'field_soccer_selected': field_soccer_selected,
            'image_base64': image_base64
        }
        return render(request, 'reservation/create.html', context)

def pay_with_card(request, id):
    reservation = Reservation.objects.get(id=id)
    email = request.user
    
    context = {
        'email': email,
        'date': reservation.date,
        'start_hour': reservation.start_hour,
        'end_hour': reservation.end_hour,
        'field_soccer_name': reservation.field_soccer.name,
        'field_soccer_number_players': reservation.field_soccer.number_players,
        'field_soccer_price': reservation.field_soccer.price,
        'field_soccer_image_base64': reservation.field_soccer.image_base64.decode("utf-8"),
        'establishment_name': reservation.field_soccer.establishment.name,
        'establishment_location': reservation.field_soccer.establishment.location,
        'establishment_phone': reservation.field_soccer.establishment.phone,
        'establishment_type_dist': reservation.field_soccer.establishment.type_dist.complete,
        'latitude': str(reservation.field_soccer.establishment.latitude).replace(',', '.'),
        'longitude': str(reservation.field_soccer.establishment.longitude).replace(',', '.')
        }
    
    if request.method == 'POST':        
        # Send Email
        email_subject = f'MiCancha - Reserva de campo deportivo para el {reservation.date} de {reservation.start_hour} a {reservation.end_hour}'
        email_template = 'send_email/reservation.html'
        email_content = render_to_string(email_template, context)
        email = EmailMessage(
            email_subject,
            email_content,
            settings.EMAIL_HOST_USER,
            ['luis.fhb.2016@gmail.com'],
        )
        email.content_subtype = 'html'
        email.send()

        reservation.type_status = TypeStatus.objects.get(id=2)
        reservation.save()

        return redirect("/reservation/")

    return render(request, 'reservation/pay_with_card.html', context)

