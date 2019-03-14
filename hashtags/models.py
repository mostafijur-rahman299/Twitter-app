# @Date:   2019-01-16T23:39:29+06:00
# @Last modified time: 2019-01-16T23:48:48+06:00

from django.db import models
from tweets.models import Tweet

# Create your models here.
class HashTag(models.Model):
    tag = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def get_tweets(self):
        return Tweet.objects.filter(content__icontains="#" + self.tag)
