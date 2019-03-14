# @Date:   2019-01-16T23:39:29+06:00
# @Last modified time: 2019-03-12T22:11:48+06:00

from django.shortcuts import render
from django.views.generic import View
from .models import HashTag
from accounts.models import UserProfileInfo

# Create your views here.
class HashTagView(View):
    def get(self,request,hashtag,*args,**kwargs):
        obj, created = HashTag.objects.get_or_create(tag=hashtag)
        profile = UserProfileInfo.objects.get(user__username__iexact=self.request.user)
        context={
            'obj': obj,
            'profile': profile
        }
        return render(request,'hashtag/hashtag.html',context)
