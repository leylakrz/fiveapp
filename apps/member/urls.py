from django.urls import path

from .views import *

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('timeline/', Timeline.as_view(), name='timeline'),
    path('users/', UserList.as_view(), name='users'),
    path('profile/<int:profile_user>/', UserProfile.as_view(), name='profile'),
    path('profile/<int:profile_user>/follow_list/', UserFollowList.as_view(), name='follow_list'),
    path('profile/<int:pk>/edit/', UserUpdate.as_view(), name='update_info'),
    path('emails/', UserEmailListJson.as_view(), name='emails'),

]
