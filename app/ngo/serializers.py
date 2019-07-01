from rest_framework import serializers
from .models import NgoDetail, Needs, Images, City, CharityHomeType

class VerifiedNeedsListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(status='verified')
        return super(VerifiedNeedsListSerializer, self).to_representation(data)


class NeedsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Needs
        fields = ('id','status','requirement')
        read_only_fields = ('id',)
        HiddenField = ('ngo',)

    def validate_status(self, value):
        if 'verified' == value.lower() or 'rejected' == value.lower() :
            raise serializers.ValidationError("Invalid status value")
        return value

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def create(self, validated_data):
        return Needs.objects.create(**validated_data,ngo=self.context['request'].user.ngo)



class NgoDetailsInlineNeedsSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = VerifiedNeedsListSerializer
        model = Needs
        fields = ('id','status','requirement')
        read_only_fields = ('id','status','requirement')

class NgoDetailsInlineImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ('id','image')
        read_only_fields = ('id','image')


class NgoDetailsSerializer(serializers.ModelSerializer):

    contactNumber = serializers.RegexField("[0-9]+",max_length=10,min_length=10)
    email = serializers.CharField(source="user.email", read_only=True)
    id = serializers.CharField(source="user.id", read_only=True)
    needs = NgoDetailsInlineNeedsSerializer(read_only=True,many=True)
    images = NgoDetailsInlineImageSerializer(read_only=True,many=True)
    city = serializers.CharField(source="city.city", read_only=True)
    charityHomeType = serializers.CharField(source="charityHomeType.charityHomeType", read_only=True)

    class Meta:
        model = NgoDetail
        fields = ('needs','id','email','name','address','city','mapLocation','description','contactNumber','charityHomeType','amountRaised','taxCertificate','images')
        read_only_fields = ('email','id','name','needs','amountRaised','images')


class NgoProfileSerializer(serializers.ModelSerializer):

    contactNumber = serializers.RegexField("[0-9]+",max_length=10,min_length=10)
    email = serializers.CharField(source="user.email", read_only=True)
    city = serializers.CharField(source="city.city", read_only=True)
    charityHomeType = serializers.CharField(source="charityHomeType.charityHomeType", read_only=True)
    id = serializers.CharField(source="user.id", read_only=True)
    needs = NeedsSerializer(read_only=True,many=True)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = NgoDetail
        fields = ('needs','id','email','name','address','city','mapLocation','description','contactNumber','charityHomeType','amountRaised','taxCertificate')
        read_only_fields = ('email','id','name','needs','amountRaised')



class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id','city')
        read_only_fields = ('id',)


class CharityHomeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharityHomeType
        fields = ('id','charityHomeType')
        read_only_fields = ('id',)





