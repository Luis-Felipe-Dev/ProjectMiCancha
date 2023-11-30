from appReservation.models import Reservation
from appUser.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

import threading
import time

def my_task():
    send_email_reminder()

def start_task():
    threading.Timer(20.0, start_task).start()
    my_task()

def send_email_reminder():
    customers = set()
    reservations = Reservation.objects.filter(date=timezone.now().date(), reminder_sent=False, type_status=2)

    for reserv in reservations:
        start_datetime = datetime.combine(timezone.now().date(), reserv.start_hour)
        time_difference = start_datetime - timezone.now()

        if timedelta(minutes=10) <= time_difference < timedelta(minutes=11):
            context = {
                    'email': User.objects.get(id=reserv.created_user),
                    'date': reserv.date,
                    'start_hour': reserv.start_hour,
                    'end_hour': reserv.end_hour,
                    'field_soccer_name': reserv.field_soccer.name,
                    'field_soccer_number_players': reserv.field_soccer.number_players,
                    'field_soccer_price': reserv.field_soccer.price,
                    'field_soccer_image_base64': reserv.field_soccer.image_base64.decode("utf-8"),
                    'establishment_name': reserv.field_soccer.establishment.name,
                    'establishment_location': reserv.field_soccer.establishment.location,
                    'establishment_phone': reserv.field_soccer.establishment.phone,
                    'establishment_type_dist': reserv.field_soccer.establishment.type_dist.complete,
                    'latitude': str(reserv.field_soccer.establishment.latitude).replace(',', '.'),
                    'longitude': str(reserv.field_soccer.establishment.longitude).replace(',', '.')
                    }
            
            # Send Email
            email_subject = f'MiCancha - Reserva de campo deportivo para el {reserv.date} de {reserv.start_hour} a {reserv.end_hour}'
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

            # Marcar la reserva como enviada
            reserv.reminder_sent = True
            reserv.save()

        customers.add(reserv.id)
