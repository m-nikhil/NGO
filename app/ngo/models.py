from django.db import models
from django.contrib.postgres.fields import ArrayField
from login.models import CustomUser

import uuid 
from django.utils.safestring import mark_safe



class LowerCaseCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(models.CharField, self).__init__(*args, **kwargs)

    # always lowercase to facilitate searching
    def get_prep_value(self, value):
        return str(value).lower()


class City(models.Model):
    id = models.AutoField(primary_key=True)
    city = LowerCaseCharField(max_length=20,unique=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.city


class CharityHomeType(models.Model):
    id = models.AutoField(primary_key=True)
    charityHomeType = LowerCaseCharField(max_length=20,unique=True)

    def __str__(self):
        return self.charityHomeType


def user_directory_path_certificate(instance, filename):
    return 'user_{0}/taxCertificate/{1}'.format(instance.name, str(uuid.uuid4()) + "." + (filename.split('.'))[-1] )

class NgoDetail(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='ngo'
    )
    name = models.CharField(max_length=20,unique=True)
    address = models.TextField(null=True,blank=True)
    city =  models.OneToOneField(City,on_delete=models.DO_NOTHING,null=True,blank=True)
    mapLocation = ArrayField(models.TextField(),size=2,null=True,blank=True)
    description = models.TextField(null=True,blank=True,max_length=1000)
    contactNumber = models.CharField(null=True,blank=True,max_length=20)
    charityHomeType = models.OneToOneField(CharityHomeType,on_delete=models.DO_NOTHING,null=True,blank=True)
    amountRaised = models.IntegerField(default = 0) 
    taxCertificate = models.FileField(null=True,blank=True,upload_to=user_directory_path_certificate)


class Needs(models.Model):

    STATUS_CHOICES = (
      ('unverified', 'unverified'),
      ('verified', 'verified'),
      ('satisfied', 'satisfied'),
      ('rejected','rejected'),
      ('deleted','deleted')
    )

    id = models.AutoField(primary_key=True)
    requirement = models.CharField(max_length=50)
    status = models.CharField(choices=STATUS_CHOICES,max_length=20,default='unverified')
    ngo = models.ForeignKey(NgoDetail, on_delete=models.CASCADE,  related_name='needs')

    class Meta:
        verbose_name_plural = "Needs"


def user_directory_path_images(instance, filename):
    return 'user_{0}/images/{1}'.format(instance.ngo.name, str(uuid.uuid4()) + "." + (filename.split('.'))[-1] )

class Images(models.Model):
    id = models.AutoField(primary_key=True)
    ngo = models.ForeignKey(NgoDetail, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=user_directory_path_images)


    class Meta:
        verbose_name_plural = "Images"


