# @Date:   2019-01-07T00:34:03+06:00
# @Last modified time: 2019-03-13T02:27:38+06:00
from django.shortcuts import render,redirect,get_object_or_404
from .models import Tweet
from django.views.generic import ListView,DetailView,UpdateView,CreateView
from django.db.models import Q
from django.http import Http404,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import TweetForm
from django import forms
from django.forms.utils import ErrorList
from django.urls import reverse
from django.views import View
from accounts.models import UserProfileInfo,UserProfile
from django.contrib.auth.models import User


class RetweetView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated:
            new_tweet = Tweet.objects.retweet(request.user, tweet)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect(tweet)

class TweetListView(LoginRequiredMixin,ListView):
    model = Tweet
    template_name = 'tweets/tweet_list.html'
    context_object_name = 'queryset'

    def get_object(self):
        return get_object_or_404(
                            User,username__iexact=self.kwargs.get('username')
                            )

    def get_context_data(self,*args,**kwargs):
        context = super(TweetListView,self).get_context_data(*args,**kwargs)
        context['create_form'] = TweetForm()
        context['create_url'] = reverse('tweets:tweet_create')
        try:
            profile = UserProfileInfo.objects.get(user__username__iexact=self.request.user)
            context['profile'] = profile
        except:
            pass
        return context

    # def get_queryset(self):
    #     qs = Tweet.objects.all().order_by('-timestamp')
    #     query = self.request.GET.get('q',None)
    #     if query is not None:
    #         qs = qs.filter(
    #             Q(user__username__iexact = query)|
    #             Q(content__icontains = query)
    #                 )
    #     return qs

# function based view
# def tweet_list(request):
#     qs = Tweet.objects.all()
#     context = {
#         'queryset':qs
#     }
#     return render(request,'tweets/tweet_list.html',context)

class TweetDetailView(DetailView):
    model = Tweet
    template_name = 'tweets/tweet_detail.html'
    context_object_name = 'object'

    def get_context_data(self,*args,**kwargs):
        context = super(TweetDetailView,self).get_context_data(*args,**kwargs)
        try:
            profile = UserProfileInfo.objects.get(user__username__iexact=self.request.user)
            context['profile'] = profile
        except:
            pass
        return context

# Function based view
# def tweet_detail(request,pk):
#     obj = Tweet.objects.get(pk=pk)
#     context = {
#         'object':obj
#     }
#     return render(request,'tweets/tweet_detail.html',context)

# class TweetDelete(DeleteView):
#     model = Tweet
#     template_name = 'tweets/tweet_c_delete.html'
#     success_url = '/'

@login_required
def tweet_delete_view(request,pk):
    try:
        tweet = Tweet.objects.get(pk=pk) # or get_object_or_404(Tweet,pk=pk)
        tweet.delete()
    except Exception as e:
        raise Http404(e)
    return redirect('tweets:tweet_list')

class TweetUpdateView(LoginRequiredMixin,UpdateView):
    model = Tweet
    template_name = 'tweets/tweet_create.html'
    form_class = TweetForm

    def form_valid(form):
        if form.instance.user == self.request.user:
            return super(TweetUpdateView,self).form_valid(form)
        else:
            form.errors[forms.forms.NON_FIELD_ERRORS]=ErrorList(['You are not instance user:)'])
            return self.form_invalid(form)

class TweetCreateView(LoginRequiredMixin,CreateView):
    model = Tweet
    template_name = 'tweets/tweet_create.html'
    form_class = TweetForm
    
    def form_valid(self,form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super(TweetCreateView,self).form_valid(form)
        else:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(['User must be login to coutinue:)'])
            return self.form_invalid(form)
