# @Date:   2019-01-12T00:36:46+06:00
# @Last modified time: 2019-03-13T04:26:58+06:00
from django.urls import path
from .views import (UserDetail,
                    UserProfileFollow,
                    register,
                    user_login,
                    user_logout,
                    UserUpdateView,
                    settings)

app_name = 'accounts'

urlpatterns = [
    path('detail/<username>/',UserDetail.as_view(),name='user_detail'),
    path('<username>/follow/',UserProfileFollow.as_view(),name='follow'),
    path('register/',register,name='register'),
    path('login/',user_login,name='user_login'),
    path('logout/',user_logout,name='user_logout'),
    path('update/<username>',UserUpdateView.as_view(),name='update'),
    path('settings/',settings,name='settings')
]
