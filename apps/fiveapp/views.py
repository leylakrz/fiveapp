from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import View
from rest_framework.views import APIView

from apps.fiveapp.forms import *
from apps.fiveapp.models import *
from apps.fiveapp.serializers import UserSerializer


class UserRegister(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'fiveapp/user_register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'fiveapp/user_register.html', {'form': form, 'message': 'ok'})
        else:
            return render(request, 'fiveapp/user_register.html', {'form': form, 'message': 'error'})


class UserLogIn(View):
    def get(self, request):
        form = UserLogInForm()
        return render(request, 'fiveapp/user_login.html', {'form': form})

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
        return render(request, 'fiveapp/user_login.html',
                      {'form': form,
                       'message': message})


class Timeline(View):
    def get(self, request, current_user):
        current_user = User.objects.get_current_user(current_user)
        return render(request, 'fiveapp/user_timeline.html', {"user": current_user})


class UserList(View):
    def get(self, request, current_user):
        user_list = User.objects.all()
        count = user_list.count()
        search_form = UserSearch()
        current_user = user_list.filter(pk=current_user)[0]
        return render(request, 'fiveapp/user_list.html', {'user_list': user_list,
                                                          'count': count,
                                                          'form': search_form,
                                                          'user': current_user})

    def post(self, request, current_user):
        current_user = User.objects.get_current_user(current_user)
        email = request.POST['email']
        user_list = User.objects.filter(email__icontains=email)
        count = user_list.count()
        if count != 1 :
            search_form = UserSearch(request.POST)
            return render(request, 'fiveapp/user_list.html', {'user_list': user_list,
                                                              'count': count,
                                                              'form': search_form,
                                                              'user': current_user})
        else:
            return redirect('profile', current_user=current_user.id, user_id=user_list[0].id)


class UserProfile(View):
    def get(self, request, current_user, user_id):
        profile_user = User.objects.get(pk=user_id)
        current_user = User.objects.get_current_user(current_user)
        posts = Post.objects.filter(publisher=profile_user)
        return render(request, 'fiveapp/user_profile.html', {'posts': posts,
                                                             'user': current_user,
                                                             'profile_user': profile_user})


class NewPostView(View):
    def get(self, request, current_user):
        form = NewPostForm()
        current_user = User.objects.get_current_user(current_user)
        return render(request, 'fiveapp/post_new.html', {
            'form': form,
            'user': current_user})

    def post(self, request, current_user):
        form = NewPostForm(request.POST)
        current_user = User.objects.get_current_user(current_user)
        if form.is_valid():
            new_post = Post(title=form.cleaned_data['title'],
                            publisher=current_user,
                            content=form.cleaned_data['content'])
            new_post.save()
            return redirect('timeline', current_user=current_user.id)
        else:
            return render(request, 'fiveapp/post_new.html', {
                'form': form,
                'user': current_user,
                'message': 'data is not valid'})


class PostDetail(View):
    def get(self, request, current_user, slug):
        post = Post.objects.get(slug=slug)
        current_user = User.objects.get_current_user(current_user)
        return render(request, 'fiveapp/post_detail.html', {'post': post,
                                                            'current_user': current_user})


class UserEmailListJson(APIView):
    def get(self, request):
        input_ = request.GET.get('input')
        emails = User.objects.filter(email__icontains=str(input_ or '')).values('email')
        serialized = UserSerializer(emails, many=True)
        return JsonResponse(serialized.data, safe=False)
