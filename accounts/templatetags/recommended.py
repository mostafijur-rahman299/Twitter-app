# @Date:   2019-01-29T22:58:42+06:00
# @Last modified time: 2019-03-12T23:52:43+06:00
from django import template
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
register = template.Library()

User = get_user_model()

@register.inclusion_tag('accounts/snipptes/recommended.html')
def recommended(user):
    if isinstance(user, User):
        qs = UserProfile.objects.recomended(user)
        return {"recomended": qs}
