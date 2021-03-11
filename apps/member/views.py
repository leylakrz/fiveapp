from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import View
from rest_framework.views import APIView

from apps.post.models import Post
from apps.member.forms import *
from apps.member.models import Follow, Member
from apps.member.serializers import UserSerializer


# Create your views here.
class UserRegister(CreateView):
    form_class = UserRegisterForm
    success_url = '/register/'
    template_name = 'user/user_register.html'

    def post(self, request):
        messages.success(request, 'User was successfully created.')
        return super(UserRegister, self).post(request)


class Timeline(LoginRequiredMixin, View):
    def get(self, request):
        followings_id = Follow.objects.filter(follower=request.user.id).values('following')
        followings = Member.objects.filter(pk__in=followings_id)
        posts = Post.objects.filter(publisher__in=followings).order_by('-publish_date')
        return render(request, 'user/user_timeline.html', {'posts': posts})


class UserList(LoginRequiredMixin, View):
    def get(self, request):
        user_list = Member.objects.all()
        count = user_list.count()
        search_form = UserSearch()
        return render(request, 'user/user_list.html', {'user_list': user_list,
                                                       'count': count,
                                                       'form': search_form, })

    def post(self, request):
        email = request.POST['email']
        user_list = Member.objects.filter(email__icontains=email)
        count = user_list.count()
        if count != 1:
            search_form = UserSearch(request.POST)
            return render(request, 'user/user_list.html', {'user_list': user_list,
                                                           'count': count,
                                                           'form': search_form, })
        else:
            return redirect('profile', profile_user=user_list[0].id)


class SetProfile:
    @staticmethod
    def set_profile(current_user, profile_user):
        profile_user = Member.objects.get(pk=profile_user)
        current_user = Member.objects.get(pk=current_user)
        following_status = Follow.objects.filter(following=profile_user, follower=current_user)
        if not following_status.exists():
            following_status = None
        else:
            following_status = following_status[0].request_accepted
        posts = Post.objects.filter(publisher=profile_user)
        return profile_user, following_status, posts


class UserProfile(LoginRequiredMixin, View, SetProfile):
    def get(self, request, profile_user):
        profile_user, following_status, posts = self.set_profile(request.user.id, profile_user)
        return render(request, 'user/user_profile.html', {'posts': posts,
                                                          'profile_user': profile_user,
                                                          'following_status': following_status})

    def post(self, request, profile_user):
        profile_user, following_status, posts = self.set_profile(request.user.id, profile_user)

        if request.POST.get('follow', False):
            # if following_status is None:
            Follow(following=profile_user, follower=request.user).save()
            return render(request, 'user/user_profile.html', {'posts': posts,
                                                              'profile_user': profile_user,
                                                              'following_status': False})

        if request.POST.get('unfollow', 'cancel_follow'):
            Follow.objects.filter(following=profile_user, follower=request.user).delete()
            return render(request, 'user/user_profile.html', {'posts': posts,
                                                              'profile_user': profile_user,
                                                              'following_status': None})


class UserEmailListJson(LoginRequiredMixin, APIView):
    def get(self, request):
        input_ = request.GET.get('input')
        emails = Member.objects.filter(email__icontains=str(input_ or '')).values('email')
        serialized = UserSerializer(emails, many=True)
        return JsonResponse(serialized.data, safe=False)


class UserFollowList(LoginRequiredMixin, View):
    def get(self, request, profile_user):
        current_user_profile = profile_user == request.user.id

        profile_user = Member.objects.get(pk=profile_user)
        profile_user_email = profile_user.email
        profile_user_id = profile_user.id

        if request.GET.get('f') == 'er':
            if current_user_profile:
                request_objects = Follow.objects.filter(following=profile_user, request_accepted=False).values(
                    'follower')
            follow_list = Follow.objects.filter(following=profile_user, request_accepted=True).values('follower')
            title = 'Follower List'

        else:
            if current_user_profile:
                request_objects = Follow.objects.filter(follower=profile_user, request_accepted=False).values(
                    'following')
            follow_list = Follow.objects.filter(follower=profile_user, request_accepted=True).values('following')
            title = 'Following List'

        user_objects = Member.objects.filter(pk__in=follow_list)

        context = {'profile_user_email': profile_user_email,
                   'profile_user_id': profile_user_id,
                   'title': title,
                   'user_objects': user_objects,
                   'f': request.GET.get('f')}
        if current_user_profile:
            context['request_objects'] = Member.objects.filter(pk__in=request_objects)

        return render(request, 'user/user_follow_list.html', context)

    def post(self, request, profile_user):
        follow_object = Follow.objects.get(following=request.user, follower__id=int(request.GET.get('request_id')))
        if request.POST.get('accept', False):
            follow_object.request_accepted = True
            follow_object.save()
        elif request.POST.get('decline', False):
            follow_object.delete()

        return self.get(request, profile_user)


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = Member
    fields = ['first_name', 'last_name', 'gender', 'website', 'bio']
    template_name = 'user/user_update.html'
