# @Date:   2019-01-16T23:59:29+06:00
# @Last modified time: 2019-01-17T00:00:37+06:00
from django.urls import path
from .views import HashTagView

app_name = 'hashtag'

urlpatterns = [
    path('<hashtag>/',HashTagView.as_view())
]
