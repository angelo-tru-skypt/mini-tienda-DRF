from rest_framework import serializers
from django.db import models
from .models import Users

class UsersSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Users
        fields = ("id", "username", "email", "password", "created_at")
        read_only_fields = ("create_at", )
    
    def create(self, validated_data):
        user = Users(
            username = validated_data["username"],
            email = validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user