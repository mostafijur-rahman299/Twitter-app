# @Date:   2019-01-22T23:45:05+06:00
# @Last modified time: 2019-01-22T23:48:21+06:00
from django.urls import path
from tweets.api.views import TweetApiSerializerView

urlpatterns = [
    path('tweets/<username>/detail/',TweetApiSerializerView.as_view(),name='Indevisual_user_tweet_list')
]
