from django.db import models
from appUser.models import User
from appFieldSoccer.models import FieldSoccer
from typeThings.models import TypeStatus

# Create your models here.
class Reservation(models.Model):
    date = models.DateField(null=False)
    start_hour = models.TimeField(null=False)
    end_hour = models.TimeField(null=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='reservation_customer')
    field_soccer = models.ForeignKey(FieldSoccer, on_delete=models.CASCADE, null=True, related_name='reservation_field_soccer')
    type_status = models.ForeignKey(TypeStatus, on_delete=models.CASCADE, null=True, related_name='reservation_type_status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    
    class Meta:
        db_table = "reservation"