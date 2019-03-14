# @Date:   2019-01-09T00:08:13+06:00
# @Last modified time: 2019-01-28T23:51:20+06:00
from django.urls import path
from .views import (TweetApiSerializerView,
                    TweetApiCreateView,
                    RetweetAPIView,
                    LikedAPIView,
                    TweetApiDetailView,
                    searchApiSerializerView,
                    hashtagTweetApiSerializerView)

urlpatterns = [
    path('tweets/list/',TweetApiSerializerView.as_view(),name='api_tweet_list'),
    path('tweets/create/',TweetApiCreateView.as_view(),name='api_tweet_create'),
    path('tweets/retweet/<int:pk>/',RetweetAPIView.as_view(),name='retweet-api'),
    path('tweets/like/<int:pk>/',LikedAPIView.as_view(),name='like'),
    path('tweets/<int:pk>/detail/',TweetApiDetailView.as_view(),name='detail'),
    path('tweets/search/',searchApiSerializerView.as_view(),name='search'),
    path('tweets/tags/<hashtag>/',hashtagTweetApiSerializerView.as_view(),name='hashtag')
]
