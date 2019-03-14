# @Date:   2019-01-09T00:31:34+06:00
# @Last modified time: 2019-03-11T12:35:10+06:00
from django.contrib import admin
from .models import UserProfile,UserProfileInfo
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserProfileInfo)
