from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserRoles(models.TextChoices):
    SUPERADMIN = 'superadmin', 'Super Admin'
    VENDOR = 'vendor', 'Vendor'
    COUNTER = 'counter', 'Counter'
    CUSTOMER = 'customer', 'Customer'

class AbstractCustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=UserRoles.choices)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_by = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'role__in': [UserRoles.SUPERADMIN, UserRoles.VENDOR, UserRoles.COUNTER, UserRoles.CUSTOMER]},
        related_name='created_users',
    )
    
    class Meta:
        abstract = True
        
class CustomUser(AbstractCustomUser):
    
    pass


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    image = models.ImageField(upload_to='media/products/', blank=True, null=True)
    detail = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role':'counter'}
        )
    
    def __str__(self):
        return f'{self.user.username} -- {self.name}'
    