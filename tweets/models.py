# @Date:   2019-01-07T00:34:03+06:00
# @Last modified time: 2019-01-29T11:27:24+06:00
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.urls import path
import re
from django.db.models.signals import post_save
from django.conf import settings
# Create your models here.

class TweetManager(models.Manager):
    def retweet(self, user, parent_obj):
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj
        qs = self.get_queryset().filter(
                                user=user,
                                parent=og_parent
                             ).filter(
                                 timestamp__year=timezone.now().year,
                                 timestamp__month=timezone.now().month,
                                 timestamp__day=timezone.now().day
                             )
        if qs.exists():
            return None
        obj = self.model(
            parent = og_parent,
            user = user,
            content = parent_obj.content
        )
        obj.save()
        return obj

    def like_toggle(self, user, like_obj):
        if user in like_obj.liked.all():
            is_liked = False
            like_obj.liked.remove(user)
        else:
            is_liked = True
            like_obj.liked.add(user)
        return is_liked

class Tweet(models.Model):
    parent      = models.ForeignKey('self',on_delete = models.CASCADE,blank=True,null=True)
    user        = models.ForeignKey(User,on_delete = models.CASCADE)
    content     = models.CharField(max_length = 140)
    liked       = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='liked',blank=True)
    reply       = models.BooleanField(verbose_name = "is reply?",default = False)
    update      = models.DateTimeField(auto_now = True)
    timestamp   = models.DateTimeField(auto_now_add = True)

    objects     = TweetManager()

    def get_absolute_url(self):
        return reverse('tweets:tweet_detail',kwargs={'pk':self.pk})

    def get_parent(self):
        the_parent = self
        if self.parent:
            the_parent = self.parent
        return the_parent

    def get_childrin(self):
        parent = self.get_parent()
        qs = Tweet.objects.filter(parent=parent)
        parent_obj = Tweet.objects.filter(pk=parent.pk)
        return (qs | parent_obj)

    def __str__(self):
        return str(self.content)
