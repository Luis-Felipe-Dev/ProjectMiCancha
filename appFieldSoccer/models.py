from django.db import models
from typeThings.models import TypeFieldSoccer
from appEstablishment.models import Establishment

# Create your models here.
class FieldSoccer(models.Model):
    name = models.CharField(max_length=150, null=False)
    number_players = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    type_field_soccer = models.ForeignKey(TypeFieldSoccer, on_delete=models.CASCADE, null=True, related_name='type_field_soccer')
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, null=True, related_name='type_field_soccer_establishment')
    status = models.BooleanField(False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    
    class Meta:
        db_table = "field_soccers"