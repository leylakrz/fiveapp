from django.urls import path

from .views import *

urlpatterns = [
    path('<int:current_user>/new_post/', NewPostView.as_view(), name='new_post'),
    path('<int:current_user>/<slug:slug>/', PostDetail.as_view(), name='post'),
]
