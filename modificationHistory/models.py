from django.db import models
from typeThings.models import TypeFieldSoccer   
from appUser.models import Rol, User
from typeThings.models import TypeDepartament, TypeProvince, TypeDistrict

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_history_users')

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
    status = models.BooleanField(False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_history_establishments')
    
    class Meta:
        db_table = "history_establishments"

class HistoryFieldSoccer(models.Model):
    name = models.CharField(max_length=150, null=False)
    number_players = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    type_field_soccer = models.ForeignKey(TypeFieldSoccer, on_delete=models.CASCADE, null=True, related_name='history_type_field_soccer')
    establishment = models.ForeignKey(HistoryEstablishment, on_delete=models.CASCADE, null=True, related_name='history_type_field_soccer_establishment')
    status = models.BooleanField(False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_history_field_soccers')
    
    class Meta:
        db_table = "history_field_soccers"

class HistoryReservation(models.Model):
    date = models.DateField(null=False)
    start_hour = models.DateTimeField(null=False)
    end_hour = models.DateTimeField(null=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='history_reservation_customer')
    field_soccer = models.ForeignKey(HistoryFieldSoccer, on_delete=models.CASCADE, null=True, related_name='history_reservation_field_soccer')
    status = models.BooleanField(False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_history_reservation')
    
    class Meta:
        db_table = "history_reservation"