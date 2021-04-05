from rest_framework import serializers

from apps.member.models import Member


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['email']
