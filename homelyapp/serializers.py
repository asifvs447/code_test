from rest_framework import serializers

from django.contrib.auth.models import User

from .models import UserProfiles, RentoutProperties, Renter

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfiles
        fields = ('account_type','phone')


class UserSerializer(serializers.ModelSerializer):
    userprofiles = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'userprofiles')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email = validated_data["email"],
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user