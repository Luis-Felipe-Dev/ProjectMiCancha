from django.db import models
from typeThings.models import TypeFieldSoccer   
from appUser.models import Rol, User
from appEstablishment.models import Establishment
from appFieldSoccer.models import FieldSoccer
from appReservation.models import Reservation
from typeThings.models import TypeDepartament, TypeProvince, TypeDistrict, TypeStatus

# Create your models here.
class HistoryUser(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=20, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=150, null=False)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, related_name='history_rol')
    last_login = None
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_id_history_users')
    user_session = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_session_history_users')

    class Meta:
        db_table = "history_users"

class HistoryEstablishment(models.Model):
    name = models.CharField(max_length=150, null=False)
    location = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=20, null=False)
    type_dep = models.ForeignKey(TypeDepartament, on_delete=models.CASCADE, null=True, related_name='history_establishment_type_dep')
    type_prov = models.ForeignKey(TypeProvince, on_delete=models.CASCADE, null=True, related_name='history_establishment_type_prov')
    type_dist = models.ForeignKey(TypeDistrict, on_delete=models.CASCADE, null=True, related_name='history_establishment_type_dist')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='history_establishment_owner')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    status = models.BooleanField(False, null=False)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, null=True, related_name='establishment_id_history_users')
    user_session = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_session_history_establishments')
    
    class Meta:
        db_table = "history_establishments"

class HistoryFieldSoccer(models.Model):
    name = models.CharField(max_length=150, null=False)
    number_players = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    type_field_soccer = models.ForeignKey(TypeFieldSoccer, on_delete=models.CASCADE, null=True, related_name='history_type_field_soccer')
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, null=True, related_name='history_type_field_soccer_establishment')
    image_base64 = models.BinaryField(null=True)
    status = models.BooleanField(False, null=False)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    field_soccer = models.ForeignKey(FieldSoccer, on_delete=models.CASCADE, null=True, related_name='field_soccer_id_history_users')
    user_session = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_session_history_field_soccers')
    
    class Meta:
        db_table = "history_field_soccers"

class HistoryReservation(models.Model):
    date = models.DateField(null=False)
    start_hour = models.DateTimeField(null=False)
    end_hour = models.DateTimeField(null=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='history_reservation_customer')
    field_soccer = models.ForeignKey(FieldSoccer, on_delete=models.CASCADE, null=True, related_name='history_reservation_field_soccer')
    type_status = models.ForeignKey(TypeStatus, on_delete=models.CASCADE, null=True, related_name='history_reservation_type_status')
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, related_name='reservation_id_history_users')
    user_session = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_session_history_reservation')
    
    class Meta:
        db_table = "history_reservation"