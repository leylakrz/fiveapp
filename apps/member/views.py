from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView
from django.views.generic.base import View
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from apps.member.forms import *
from apps.member.models import Follow, Member
from apps.member.serializers import UserSerializer
from apps.post.models import Post
from .tokens import account_activation_token
from common.sms import send_sms
from ..event.models import Event


class Register(View):
    """
    creates a new member (not activated) and sends authentication email (containing activation link) or
    sms (containing a 4-digit code) depending on member's preference.
    if successful, redirects to sms confirmation page or a page informing the member to check their email.
    """

    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'user/registration_form.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            current_site = get_current_site(request)

            if request.POST['auth_method'] == 'email':
                mail_subject = 'Activate your account on {}.'.format(current_site.domain)
                message = render_to_string('user/acc_active_email.html', {
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)).encode().decode(),
                    'token': account_activation_token.make_token(new_user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')

            # elif request.POST['auth_method'] == 'sms':
            send_sms(phone_number=new_user.phone_number, sms_code=new_user.sms_code)
            return redirect('/sms_confirmation/{}/'.format(str(new_user.id)))

        return render(request, 'user/registration_form.html', {'form': form})


def email_confirmation(request, uidb64, token):
    """
    called when user clicks on activation link sent to their email address. if the link is valid, their account is
    activated.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Member.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Member.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(reverse('login'))
    else:
        return HttpResponse('Activation link is invalid!')


class UserSmsConfirmation(View):
    """
    gets the 4-digit code sms sent to member's phone number and check if typed code is correct. member can ask for
    another sms.
    """

    def get(self, request, user_id):
        form = UserSmsAuthentication()
        return render(request, 'user/user_authentication.html', {'form': form,
                                                                 'title': 'user sms authentication',
                                                                 'user_id': user_id})

    def post(self, request, user_id):
        member = Member.objects.get(pk=user_id)
        send_again = request.GET.get('send_again', False)
        if not send_again:
            sms_code = request.POST.get('sms_code', False)
            if member.sms_code == sms_code:
                return redirect('login')
            else:
                form = UserSmsAuthentication(request.POST)
                return render(request, 'user/user_authentication.html', {'form': form,
                                                                         'title': 'user sms authentication',
                                                                         'user_id': user_id,
                                                                         'message': 'code is not correct.'})

        send_sms(phone_number=member.phone_number, sms_code=member.sms_code)
        return self.get(request, user_id)


class Timeline(LoginRequiredMixin, View):
    """
    returns all the posts published by member's followings, ordered by publishing date and time (descending).
    """

    def get(self, request):
        followings_id = Follow.objects.filter(follower=request.user.id).values('following')
        followings = Member.objects.filter(pk__in=followings_id)
        posts = Post.objects.filter(publisher__in=followings).order_by('-publish_date')
        return render(request, 'user/user_timeline.html', {'posts': posts})


class UserList(LoginRequiredMixin, View):
    """
    returns list of members and their total count.
    there's a search form that enables member to search among all members. if there's only one result for search,
    member will be redirected to result's profile. else, matching results will be shown along with the count.
    """

    def get(self, request):
        user_list = Member.objects.all()
        count = user_list.count()
        return render(request, 'user/user_list.html', {'user_list': user_list,
                                                       'count': count, })

    def post(self, request):
        email = request.POST['email']
        user_list = Member.objects.filter(email__icontains=email)
        count = user_list.count()
        if count != 1:
            return render(request, 'user/user_list.html', {'user_list': user_list,
                                                           'count': count,
                                                           'email': email})
        else:
            return redirect('profile', profile_user=user_list[0].id)


class UserEmailListJson(LoginRequiredMixin, APIView):
    """
    returns list of all members' email in json format. user in autocomplete javascript code in 'user/user_list.html'
    """
    def get(self, request):
        input_ = request.GET.get('input')
        emails = Member.objects.filter(email__icontains=str(input_ or '')).values('email')
        serialized = UserSerializer(emails, many=True)
        return JsonResponse(serialized.data, safe=False)


class SetProfile:
    """
    not a view, defined just for a cleaner code. used in UserProfile view.
    gets ids of logged in member and the member their profile being visit.
    returns some profile infos such as:
        whether visitor is a follower of has requested for follow or is not a follower,
        profile member's full name, gender, registration date, website link and biography.
        profile member's published posts.
    """

    @staticmethod
    def set_profile(current_user, profile_user):
        profile_user = Member.objects.get(pk=profile_user)
        current_user = Member.objects.get(pk=current_user)
        following_status = Follow.objects.filter(following=profile_user, follower=current_user)
        if not following_status.exists():
            following_status = None
        else:
            following_status = following_status[0].request_accepted
        posts = Post.objects.filter(publisher=profile_user).order_by('-id')
        return profile_user, following_status, posts


class UserProfile(LoginRequiredMixin, View, SetProfile):
    """
    returns profile info.
    gets id of the member their profile being visit.
    """

    def get(self, request, profile_user):
        profile_user, following_status, posts = self.set_profile(request.user.id, profile_user)
        return render(request, 'user/user_profile.html', {'posts': posts,
                                                          'profile_user': profile_user,
                                                          'following_status': following_status})

    def post(self, request, profile_user):
        profile_user, following_status, posts = self.set_profile(request.user.id, profile_user)

        # if member is visiting someone else's profile and is not following them, the button 'follow' is shown.
        # a new follow object is created, with visitor being the following and profile's member being the follower.
        # follow object's request_accepted field is false by default, which means follower must wait for the following
        # to decide. if follower accepts the request, request_accepted will become true. otherwise, this object will
        # deleted.
        # the new event object will inform the following that a new following request has been registered.
        if request.POST.get('follow', False):
            Follow(following=profile_user, follower=request.user).save()
            Event(operator=request.user, viewer=profile_user, type='follow', ).save()
            return render(request, 'user/user_profile.html', {'posts': posts,
                                                              'profile_user': profile_user,
                                                              'following_status': False})

        # if the following take back their follow request before the follower decides about it,
        # or the following unfollows the follower after their follow request was accepted,
        # the follow object and the event informing the following they have had a follow request and the event
        # informing the follower their follow request has been accepted will be deleted from database.
        if request.POST.get('unfollow', 'cancel_follow'):
            Follow.objects.filter(following=profile_user, follower=request.user).delete()
            Event.objects.filter(operator=request.user, viewer=profile_user, type='follow').delete()
            Event.objects.filter(operator=profile_user, viewer=request.user, type='accept').delete()
            return render(request, 'user/user_profile.html', {'posts': posts,
                                                              'profile_user': profile_user,
                                                              'following_status': None})


class UserFollowList(LoginRequiredMixin, View):
    """
    returns list of members a certain member follows or is followed by.
    if a member is visiting their own follow/following list, they can also see the follow request they have registered
    or received. if they have received any follow requests, they can accept or deny it. by accepting a request the
    related follow object's request_accepted field is valued as true. in case of decline, follow object is deleted.
    """
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
        follower_id = int(request.GET.get('request_id'))
        follow_object = Follow.objects.get(following=request.user, follower__id=follower_id)

        if request.POST.get('accept', False):
            follow_object.request_accepted = True
            follow_object.save()
            Event(operator=request.user, viewer=Member.objects.get(pk=follower_id),
                  type='accept', ).save()

        elif request.POST.get('decline', False):
            follow_object.delete()
            Event.objects.filter(operator=request.user, viewer=profile_user, type='follow').delete()

        return self.get(request, profile_user)


class UserUpdate(LoginRequiredMixin, UpdateView):
    """
    enables each member to edit their name, gender, website link and biography.
    """
    model = Member
    fields = ['first_name', 'last_name', 'gender', 'website', 'bio']
    template_name = 'user/user_update.html'
