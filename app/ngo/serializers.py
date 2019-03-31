from rest_framework import serializers
from .models import NgoDetail, Needs

class VerifiedNeedsListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(status='verified')
        return super(VerifiedNeedsListSerializer, self).to_representation(data)


class NeedsSerailizer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = VerifiedNeedsListSerializer
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



class NgoDetailsInlineNeedsSerailizer(serializers.ModelSerializer):

    class Meta:
        model = Needs
        fields = ('id','status','requirement')
        read_only_fields = ('id','status','requirement')

class NgoDetailsSerailizer(serializers.ModelSerializer):

    contactNumber = serializers.RegexField("[0-9]+",max_length=10,min_length=10)
    email = serializers.CharField(source="user.email", read_only=True)
    id = serializers.CharField(source="user.id", read_only=True)
    needs = NgoDetailsInlineNeedsSerailizer(read_only=True,many=True)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = NgoDetail
        fields = ('needs','id','email','name','address','city','mapLocation','description','contactNumber','charityHomeType','amountRaised','taxCertificate')
        read_only_fields = ('email','id','name','needs')




