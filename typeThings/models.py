from django.db import models

# Create your models here.
class TypeFieldSoccer(models.Model):
    description = models.CharField(max_length=100, null=False)
    status = models.BooleanField(False, null=False)
    
    class Meta:
        db_table = "type_field_soccer"

class TypeDepartament(models.Model):
    description = models.CharField(max_length=150, null=False)
    status = models.BooleanField(default=True, null=False)
    
    class Meta:
        db_table = "type_department"

class TypeProvince(models.Model):
    description = models.CharField(max_length=150, null=False)
    relation = models.ForeignKey(TypeDepartament, on_delete=models.CASCADE, null=True, related_name='relation_departament')
    ubigeo = models.CharField(max_length=10, null=False)
    complete = models.CharField(max_length=200, null=False)
    status = models.BooleanField(default=True, null=False)

    class Meta:
        db_table = "type_province"

class TypeDistrict(models.Model):
    description = models.CharField(max_length=150, null=False)
    relation = models.ForeignKey(TypeProvince, on_delete=models.CASCADE, null=True, related_name='relation_province')
    ubigeo = models.CharField(max_length=10, null=False)
    complete = models.CharField(max_length=200, null=False)
    status = models.BooleanField(default=True, null=False)
    
    class Meta:
        db_table = "type_district"