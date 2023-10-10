from django.db import models
from appUser.models import User

# Create your models here.
class Establishment(models.Model):
    name = models.CharField(max_length=150, null=False)
    location = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=20, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='establishment_owner')
    status = models.BooleanField(False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    created_user = models.IntegerField(null=True)
    updated_user = models.IntegerField(null=True)
    deleted_user = models.IntegerField(null=True)
    
    class Meta:
        db_table = "establishments"