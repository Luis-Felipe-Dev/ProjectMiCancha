from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from typeThings.models import TypeDepartament, TypeProvince, TypeDistrict

# Create your models here.
class Rol(models.Model):
    description = models.CharField(max_length=100, null=False)
    status = models.BooleanField(False, null=False)
    
    class Meta:
        db_table = "roles"

class CustomerUser(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    type_dep = models.ForeignKey(TypeDepartament, on_delete=models.CASCADE, null=True, related_name='user_type_dep')
    type_prov = models.ForeignKey(TypeProvince, on_delete=models.CASCADE, null=True, related_name='user_type_prov')
    type_dist = models.ForeignKey(TypeDistrict, on_delete=models.CASCADE, null=True, related_name='user_type_dist')
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=20, null=False)
    email = models.EmailField(unique=True, null=False)
    # username = models.CharField(max_length=150, unique=True, null=False)
    password = models.CharField(max_length=150, null=False)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, related_name='rol')
    last_login = None
    full_name_emergency_contact = models.CharField(max_length=150, null=True)
    phone_emergency_contact = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)

    USERNAME_FIELD = 'email'

    objects = CustomerUser()

    class Meta:
        db_table = "users"