# @Date:   2019-01-08T20:46:24+06:00
# @Last modified time: 2019-01-21T22:49:54+06:00
from django.urls import path
from .views import (TweetListView,
                    TweetDetailView,
                    tweet_delete_view,
                    TweetUpdateView,
                    TweetCreateView,
                    RetweetView)
from django.views.generic import RedirectView

app_name = 'tweets'

urlpatterns = [
    path('',RedirectView.as_view(url='/'),name='tweet_list'),
    path('detail/<int:pk>/',TweetDetailView.as_view(),name='tweet_detail'),
    path('retweet/<int:pk>/',RetweetView.as_view(),name='retweet'),
    path('remove/<int:pk>/',tweet_delete_view,name='tweet_remove'),
    path('create/',TweetCreateView.as_view(),name='tweet_create'),
    path('update/<int:pk>/',TweetUpdateView.as_view(),name='tweet_create'),
]
