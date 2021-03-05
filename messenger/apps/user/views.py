from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View
from rest_framework.views import APIView

from apps.post.models import Post
from apps.user.forms import *
from apps.user.models import Follow, User
from apps.user.serializers import UserSerializer


class UserRegister(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'user/user_register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'user/user_register.html', {'form': form, 'message': 'ok'})
        else:
            return render(request, 'user/user_register.html', {'form': form, 'message': 'error'})


class UserLogIn(View):
    def get(self, request):
        form = UserLogInForm()
        return render(request, 'user/user_login.html', {'form': form})

    def post(self, request):
        user = User.objects.log_in(request.POST)
        # check email
        if user is not None:
            # check password
            if user:
                # return render(request, 'fiveapp/user_timeline.html', {'user': user})
                return redirect('timeline', current_user=user.id)
            else:
                message = 'Wrong Password.'
        else:
            message = 'There Is No Account With This Email.'

        form = UserLogInForm(request.POST)
        return render(request, 'user/user_login.html',
                      {'form': form,
                       'message': message})


class Timeline(View):
    def get(self, request, current_user):
        current_user = User.objects.get(pk=current_user)
        followings_id = Follow.objects.filter(follower=current_user).values('following')
        followings = User.objects.filter(pk__in=followings_id)
        posts = Post.objects.filter(publisher__in=followings).order_by('-publish_date')
        return render(request, 'user/user_timeline.html', {"user": current_user,
                                                           'posts': posts})


class UserList(View):
    def get(self, request, current_user):
        user_list = User.objects.all()
        count = user_list.count()
        search_form = UserSearch()
        current_user = user_list.filter(pk=current_user)[0]
        return render(request, 'user/user_list.html', {'user_list': user_list,
                                                       'count': count,
                                                       'form': search_form,
                                                       'user': current_user})

    def post(self, request, current_user):
        current_user = User.objects.get(pk=current_user)
        email = request.POST['email']
        user_list = User.objects.filter(email__icontains=email)
        count = user_list.count()
        if count != 1:
            search_form = UserSearch(request.POST)
            return render(request, 'user/user_list.html', {'user_list': user_list,
                                                           'count': count,
                                                           'form': search_form,
                                                           'user': current_user})
        else:
            return redirect('profile', current_user=current_user.id, profile_user=user_list[0].id)


class SetProfile:
    @staticmethod
    def set_profile(current_user, profile_user):
        profile_user = User.objects.get(pk=profile_user)
        current_user = User.objects.get(pk=current_user)
        following_status = Follow.objects.filter(following=profile_user, follower=current_user)
        posts = Post.objects.filter(publisher=profile_user)
        return profile_user, current_user, bool(following_status), posts


class UserProfile(View, SetProfile):
    def get(self, request, current_user, profile_user):
        profile_user, current_user, following_status, posts = self.set_profile(current_user, profile_user)
        return render(request, 'user/user_profile.html', {'posts': posts,
                                                          'user': current_user,
                                                          'profile_user': profile_user,
                                                          'following_status': following_status})


class UserFollow(View, SetProfile):
    def get(self, request, current_user, profile_user):
        profile_user, current_user, following_status, posts = self.set_profile(current_user, profile_user)
        if not following_status:
            Follow(following=profile_user, follower=current_user).save()
        return render(request, 'user/user_profile.html', {'posts': posts,
                                                          'user': current_user,
                                                          'profile_user': profile_user,
                                                          'following_status': True})


class UserUnfollow(View, SetProfile):
    def get(self, request, current_user, profile_user):
        profile_user, current_user, following_status, posts = self.set_profile(current_user, profile_user)
        if following_status:
            Follow.objects.filter(following=profile_user, follower=current_user).delete()
        return render(request, 'user/user_profile.html', {'posts': posts,
                                                          'user': current_user,
                                                          'profile_user': profile_user,
                                                          'following_status': False})


class UserEmailListJson(APIView):
    def get(self, request):
        input_ = request.GET.get('input')
        emails = User.objects.filter(email__icontains=str(input_ or '')).values('email')
        serialized = UserSerializer(emails, many=True)
        return JsonResponse(serialized.data, safe=False)


class UserFollowList(View):
    def get(self, request, current_user, profile_user):
        current_user = User.objects.get(pk=current_user)
        profile_user_email = User.objects.get(pk=profile_user).email
        if request.GET.get('f') == 'er':
            follow_list = Follow.objects.filter(following=profile_user).values('follower')
            title = 'Follower List'
        else:
            follow_list = Follow.objects.filter(follower=profile_user).values('following')
            title = 'Following List'

        user_objects = User.objects.filter(pk__in=follow_list)
        return render(request, 'user/user_follow_list.html', {'user': current_user,
                                                              'profile_user_email': profile_user_email,
                                                              'title': title,
                                                              'user_objects': user_objects})
