from django.urls import path

from .views import *

urlpatterns = [
    path('', UserLogIn.as_view(), name='login'),
    path('register/', UserRegister.as_view(), name='register'),
    path('<int:current_user>/timeline/', Timeline.as_view(), name='timeline'),
    path('<int:current_user>/users/', UserList.as_view(), name='users'),
    path('<int:current_user>/profile/<int:profile_user>/', UserProfile.as_view(), name='profile'),
    path('<int:current_user>/profile/<int:profile_user>/f', UserFollow.as_view(), name='follow'),
    path('<int:current_user>/profile/<int:profile_user>/u', UserUnfollow.as_view(), name='unfollow'),
    path('<int:current_user>/profile/<int:profile_user>/follow_list', UserFollowList.as_view(), name='follow_list'),
    path('emails/', UserEmailListJson.as_view(), name='emails'),
]
