# @Date:   2019-01-09T00:31:34+06:00
# @Last modified time: 2019-03-13T04:36:23+06:00
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import DetailView,View,ListView,UpdateView
from django.contrib.auth import get_user_model
from .models import UserProfile,UserProfileInfo
from .forms import UserForm,UserProfileInfoForm,LoginForm
from  django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.utils import ErrorList
from .models import UserProfileInfo
from django.contrib.auth.models import User
from .forms import UserForm,UserProfileInfoForm
from django.urls import reverse_lazy

User = get_user_model()

class UserDetail(DetailView):
    queryset = User.objects.all()
    template_name = 'accounts/user_detail.html'

    def get_object(self):
        return get_object_or_404(
                            User,username__iexact=self.kwargs.get('username')
                            )

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetail, self).get_context_data(*args,**kwargs)
        following = UserProfile.objects.is_following(self.request.user, self.get_object())
        context['following'] = following
        context['recomended'] = UserProfile.objects.recomended(self.request.user)
        try:
            profile = UserProfileInfo.objects.get(user__username__iexact=self.kwargs.get('username'))
            context['profile'] = profile
        except:
            pass
        return context

class UserProfileFollow(View):
    def get(self, request, username, *args,**kwargs):
        toggle_user = get_object_or_404(User,username__iexact = username)
        if request.user.is_authenticated:
            is_following = UserProfile.objects.toggle_follow(request.user,toggle_user)
        return redirect('accounts:user_detail',username=username)

def register(request):

    registered=False
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user


            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()
            registered=True

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
    return render(request,'accounts/register.html',{'user_form':user_form,
                                                    'profile_form':profile_form,
                                                    'registered':registered})


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST or None)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request,user)
                return redirect('/')
            else:
                pass
    else:
        login_form = LoginForm()
    return render(request, 'accounts/login.html',{'login_form': login_form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')

class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    template_name = 'accounts/settings/update.html'
    fields = [
        'username',
        'email',
    ]
    def get_success_url(self):
        return reverse_lazy('accounts:user_detail', kwargs={'username': self.request.user})

    def get_object(self):
        return get_object_or_404(
                            User,username__iexact=self.kwargs.get('username')
                            )



    def get_object(self):
        return get_object_or_404(
                            User,username__iexact=self.kwargs.get('username')
                            )

def settings(request):
    return render(request,'accounts/settings/settings.html')
