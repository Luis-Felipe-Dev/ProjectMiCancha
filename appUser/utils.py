import random
from django.conf import global_settings
from django.core.mail import send_mail

def generate_password():
    characters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()?><:;')
    length = 10

    password = ''
    for x in range(length):
        password += random.choice(characters)

    return password

def send_gmail(subject, message, recipient_list):
    subject = subject
    message = message
    email_from = global_settings.EMAIL_HOST_USER
    recipient_list = recipient_list
    send_mail(subject, message, email_from, recipient_list)

