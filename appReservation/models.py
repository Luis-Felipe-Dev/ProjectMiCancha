from django.db import models
from appUser.models import User
from appFieldSoccer.models import FieldSoccer

# Create your models here.
class Reservation(models.Model):
    date = models.DateField(null=False)
    start_hour = models.DateTimeField(null=False)
    end_hour = models.DateTimeField(null=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='reservation_customer')
    field_soccer = models.ForeignKey(FieldSoccer, on_delete=models.CASCADE, null=True, related_name='reservation_field_soccer')
    status = models.BooleanField(False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    
    class Meta:
        db_table = "reservation"