# @Date:   2019-01-09T00:08:07+06:00
# @Last modified time: 2019-01-28T23:53:40+06:00
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView
from .serializers import TweetApiSerializer
from tweets.models import Tweet
from django.db.models import Q
from rest_framework import permissions
from .pagination import StandartResultpagination
from rest_framework.views import APIView
from rest_framework.response import Response
from hashtags.models import HashTag

class LikedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    message = 'Not allowed'
    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        if request.user.is_authenticated:
            is_liked = Tweet.objects.like_toggle(request.user, tweet_qs.first())
            return Response({'liked':is_liked})
        return Response({'message':message}, status=400)

class RetweetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    message = 'Not allowed'
    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        if tweet_qs.exists() and tweet_qs.count() == 1:
            new_tweet = Tweet.objects.retweet(request.user, tweet_qs.first())
            if new_tweet:
                data = TweetApiSerializer(new_tweet).data
                return Response(data)
            message = "Can't retweet the same in one day"
        return Response({'message':message},status=400)

class TweetApiCreateView(CreateAPIView):
    serializer_class = TweetApiSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class TweetApiDetailView(ListAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetApiSerializer
    pagination_class = StandartResultpagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        tweet_id = self.kwargs.get('pk')
        qs = Tweet.objects.filter(pk=tweet_id)
        if qs.exists() and qs.count() == 1:
            parent_obj = qs.first()
            qs1 = parent_obj.get_childrin()
            qs = (qs | qs1).distinct().extra(select={'parent_id_null':'parent_id IS Null'})
        return qs.order_by('-parent_id_null','-timestamp')

class hashtagTweetApiSerializerView(ListAPIView):
    queryset = Tweet.objects.all().order_by('-timestamp')
    serializer_class = TweetApiSerializer
    pagination_class = StandartResultpagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(hashtagTweetApiSerializerView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self):
        hashtag = self.kwargs.get('hashtag')
        hashtag_obj = None
        try:
            hashtag_obj = HashTag.objects.get_or_create(tag=hashtag)[0]
        except:
            pass
        if hashtag_obj:
            qs = hashtag_obj.get_tweets()
            query = self.request.GET.get('q')
            if query is not None:
                qs = qs.filter(
                    Q(user__username__icontains = query)|
                    Q(content__icontains = query)
                    )
            return qs
        return None


class searchApiSerializerView(ListAPIView):
    queryset = Tweet.objects.all().order_by('-timestamp')
    serializer_class = TweetApiSerializer
    pagination_class = StandartResultpagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(searchApiSerializerView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self):
        qs = self.queryset
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                Q(user__username__icontains = query)|
                Q(content__icontains = query)
                )
        return qs

class TweetApiSerializerView(ListAPIView):
    serializer_class = TweetApiSerializer
    pagination_class = StandartResultpagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(TweetApiSerializerView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self):
        requested_user = self.kwargs.get('username')
        if requested_user:
            qs = Tweet.objects.filter(user__username=requested_user).order_by('-timestamp')
        else:
            im_following = self.request.user.profile.get_following()
            qs1 = Tweet.objects.filter(user__in=im_following).order_by('-timestamp')
            qs2 = Tweet.objects.filter(user = self.request.user)
            qs = (qs1 | qs2).distinct().order_by('-timestamp')
        query = self.request.GET.get('q',None)
        if query is not None:
            qs = qs.filter(
                Q(user__username__icontains = query)|
                Q(content__icontains = query)
                )
        return qs
