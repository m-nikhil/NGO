from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from . manager import CustomUserManager


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    username = None
    first_name = None
    last_name = None
    is_ngo =  models.BooleanField(default=False)

    email = models.EmailField(unique=True)
    modified_by = models.EmailField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    firstName =  models.CharField(max_length=20)
    lastName =  models.CharField(max_length=20)
    dateOfBirth = models.DateField()
    phoneNumber = models.CharField(max_length=20)
    PanNumber = models.CharField(max_length=20,null=True,blank=True)


class Ngo(CustomUser):
    class Meta:
        proxy = True


class Staff(CustomUser):
    class Meta: 
        proxy = True
