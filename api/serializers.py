from rest_framework import serializers
from .models import Audio, FIR
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import PoliceOfficer


class PoliceOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceOfficer
        fields = ["id", "full_name", "uid", "phone"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = PoliceOfficer
        fields = ["full_name", "uid", "phone", "password"]

    def create(self, validated_data):
        officer = PoliceOfficer.objects.create_user(**validated_data)
        return officer


class LoginSerializer(serializers.Serializer):
    uid = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        officer = authenticate(uid=data["uid"], password=data["password"])
        if not officer:
            raise serializers.ValidationError("Invalid UID or password")

        refresh = RefreshToken.for_user(officer)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": PoliceOfficerSerializer(officer).data
        }


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'


class FIRSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIR
        fields = '__all__'
