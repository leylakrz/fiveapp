from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

from apps.post.froms import *
from apps.user.models import User


class NewPostView(View):
    def get(self, request, current_user):
        form = NewPostForm()
        current_user = User.objects.get(pk=current_user)
        return render(request, 'post/post_new.html', {
            'form': form,
            'user': current_user})

    def post(self, request, current_user):
        form = NewPostForm(request.POST)
        current_user = User.objects.get(pk=current_user)
        if form.is_valid():
            new_post = Post(title=form.cleaned_data['title'],
                            publisher=current_user,
                            content=form.cleaned_data['content'])
            new_post.save()
            return redirect('timeline', current_user=current_user.id)
        else:
            return render(request, 'post/post_new.html', {
                'form': form,
                'user': current_user,
                'message': 'data is not valid'})


class PostDetail(View):
    def get(self, request, current_user, slug):
        post = Post.objects.get(slug=slug)
        current_user = User.objects.get(pk=current_user)
        comments = Comment.objects.filter(post=post)
        comment_form = CommentForm()
        return render(request, 'post/post_detail.html', {'post': post,
                                                         'user': current_user,
                                                         'comment_form': comment_form,
                                                         'comments': comments})

    def post(self, request, current_user, slug):
        current_user = User.objects.get(pk=current_user)
        post = Post.objects.get(slug=slug)

        if request.POST.get('like', False):
            if current_user not in post.liked.all():
                post.liked.add(current_user)
                post.save()

        comment_form = CommentForm(request.POST)
        if request.POST.get('comment', False):
            Comment(publisher=current_user,
                    post=post,
                    title=request.POST['title'],
                    content=request.POST['content'],
                    ).save()
            comment_form = CommentForm()
        comments = Comment.objects.filter(post=post)

        return render(request, 'post/post_detail.html', {'post': post,
                                                         'user': current_user,
                                                         'comment_form': comment_form,
                                                         'comments': comments})
