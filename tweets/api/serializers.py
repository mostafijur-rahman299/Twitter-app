# @Date:   2019-01-09T00:07:49+06:00
# @Last modified time: 2019-01-26T21:40:07+06:00
from rest_framework import serializers
from django.utils.timesince import timesince
from tweets.models import Tweet
from accounts.api.serializers import SerializerUser

class parentTweetApiSerializer(serializers.ModelSerializer):
    user = SerializerUser(read_only = True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()


    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'update',
            'timestamp',
            'date_display',
            'timesince',

        ]


    def get_date_display(self, obj):
        return obj.timestamp.strftime("%d %b %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

class TweetApiSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(write_only=True, required=False)
    user = SerializerUser(read_only = True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    parent = parentTweetApiSerializer(read_only=True)
    likes = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'parent_id',
            'id',
            'user',
            'content',
            'update',
            'timestamp',
            'date_display',
            'timesince',
            'parent',
            'likes',
            'did_like',
            'reply'
        ]
        #read_only_fields = ['reply']

    def get_did_like(self, obj):
        request = self.context.get('request')
        user = request.user
        if user in obj.liked.all():
            return True
        return False


    def get_likes(self, obj):
        return obj.liked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%d %b %y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"
