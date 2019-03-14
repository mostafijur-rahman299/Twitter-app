# @Date:   2019-01-09T00:31:34+06:00
# @Last modified time: 2019-03-13T03:16:06+06:00
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save


class UserProfileManager(models.Manager):
    use_for_related_fields = True
    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, toggle_follow_user):
        user_profile, created = UserProfile.objects.get_or_create(user = user)
        if toggle_follow_user in user_profile.following.all():
            user_profile.following.remove(toggle_follow_user)
            added = False
        else:
            user_profile.following.add(toggle_follow_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user = user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False

    def recomended(self, user, limit_to=10):
        profile = user.profile
        following = profile.following.all()
        following = profile.get_following()
        qs = self.get_queryset().exclude(user__in=following).exclude(id=profile.id).order_by("?")[:limit_to]
        return qs

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,related_name='profile')
    following = models.ManyToManyField(User,related_name = 'followed_by',blank=True)

    objects = UserProfileManager()

    def __str__(self):
        return str(self.following.all().count())

    def get_following(self):
        return self.following.all().exclude(username = self.user.username)

    def get_follow_url(self, *args, **kwargs):
        return reverse('accounts:follow',kwargs={'username':self.user.username})

    def get_absolute_url(self):
        return reverse('accounts:user_detail',kwargs={'username':self.user.username})

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        new_profile = UserProfile.objects.get_or_create(user = instance)

post_save.connect(post_save_user_receiver, sender = User)

class UserProfileInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    portfolio_site=models.URLField(blank=True, null=True)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return redirect('/accounts/detail/{{ requset.user }}')
