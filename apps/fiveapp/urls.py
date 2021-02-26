from django.urls import path

from .views import *

urlpatterns = [
    path('', UserLogIn.as_view(), name='login'),
    path('register/', UserRegister.as_view(), name='register'),
    path('<int:current_user>/timeline/', Timeline.as_view(), name='timeline'),
    path('<int:current_user>/users/', UserList.as_view(), name='users'),
    path('<int:current_user>/profile/<int:user_id>/', UserProfile.as_view(), name='profile'),
    path('<int:current_user>/new_post/', NewPostView.as_view(), name='new_post'),
    path('<int:current_user>/<slug:slug>/', PostDetail.as_view(), name='post'),
    path('emails/', UserEmailListJson.as_view(), name='emails'),
]
