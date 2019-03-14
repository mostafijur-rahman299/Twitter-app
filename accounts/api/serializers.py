# @Date:   2019-01-09T00:34:05+06:00
# @Last modified time: 2019-03-11T12:30:31+06:00
from rest_framework import serializers
from django.contrib.auth.models import User
from django.urls import reverse

class SerializerUser(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'follower',
            'url'
        ]

    def get_follower(self,obj):
        return 0
    def get_url(self,obj):
        return reverse('accounts:user_detail',kwargs={'username':obj.username})
