from django.urls import path

from .views import *

urlpatterns = [
    path('new_post/', NewPostView.as_view(), name='new_post'),
    path('<slug:slug>/', PostDetail.as_view(), name='post'),
    path('<slug:slug>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('<slug:slug>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<slug:slug>/likes/', PostLikedList.as_view(), name='likes'),
]
