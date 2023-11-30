from django.db import models
from appUser.models import User
from typeThings.models import TypeDepartament, TypeProvince, TypeDistrict

# Create your models here.
class Establishment(models.Model):
    name = models.CharField(max_length=150, null=False)
    location = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=20, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='establishment_owner')
    type_dep = models.ForeignKey(TypeDepartament, on_delete=models.CASCADE, null=True, related_name='establishment_type_dep')
    type_prov = models.ForeignKey(TypeProvince, on_delete=models.CASCADE, null=True, related_name='establishment_type_prov')
    type_dist = models.ForeignKey(TypeDistrict, on_delete=models.CASCADE, null=True, related_name='establishment_type_dist')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    status = models.BooleanField(False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    
    class Meta:
        db_table = "establishments"