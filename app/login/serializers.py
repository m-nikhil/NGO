from rest_framework import serializers
from .models import CustomUser, UserProfile
from rest_framework.validators import UniqueValidator
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from django.db import transaction, DatabaseError
from rest_framework.response import Response
from rest_framework.exceptions import server_error
from django.contrib.auth.hashers import make_password

class  UserProfileSerailizer(serializers.ModelSerializer):
    
    phoneNumber = serializers.RegexField("[0-9]+",max_length=10,min_length=10)
    user = serializers.SlugRelatedField( read_only=True, slug_field='email')

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ('user','firstName','lastName','dateOfBirth','phoneNumber','PanNumber')
        read_only_fields = ('user' , 'firstName','lastName')

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(min_length=6)
    firstName = serializers.RegexField("[a-zA-Z]+")
    LastName = serializers.RegexField("[a-zA-Z]+")
    confirmpassword = serializers.CharField()
    dateOfBirth = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    panNumber = serializers.CharField()
    phoneNumber = serializers.RegexField("[0-9]+",max_length=10,min_length=10)

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        confirmpassword = validated_data.get('confirmpassword')
        firstName = validated_data.get('firstName')
        lastName = validated_data.get('LastName')
        dateOfBirth = validated_data.get('dateOfBirth')
        panNumber = validated_data.get('panNumber')
        phoneNumber = validated_data.get('phoneNumber')

        if(password!=confirmpassword):
            raise serializers.ValidationError("Confirm password doesn't match the entered password")

        user = None
        try:
            with transaction.atomic():
                user = CustomUser.objects.create(email=email,password=make_password(password),first_name=firstName,last_name=lastName)
                UserProfile.objects.create(user=user,dateOfBirth=dateOfBirth,PanNumber=panNumber,phoneNumber=phoneNumber)
        except DatabaseError:
                raise server_error

        return user


    class Meta:
        model = CustomUser
        fields = ('email','password','first_name','last_name')


