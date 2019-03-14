# @Date:   2019-01-28T22:38:20+06:00
# @Last modified time: 2019-01-28T22:52:42+06:00

from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q',None)
        qs = User.objects.all()
        if query is not None:
            qs = qs.filter(
                Q(username__icontains=query)
            )
        context = {
            'users':qs
        }
        return render(request, 'tweets/search.html',context)
