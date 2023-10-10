from django.db import models

# Create your models here.
class TypeFieldSoccer(models.Model):
    description = models.CharField(max_length=100, null=False)
    status = models.BooleanField(False, null=False)
    
    class Meta:
        db_table = "type_field_soccer"