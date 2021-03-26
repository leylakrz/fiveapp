from django.conf.urls import url
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from django.views.generic.base import View

from apps.post.forms import *


class NewPostView(LoginRequiredMixin, View):
    def get(self, request):
        form = NewPostForm()
        return render(request, 'post/post_new.html', {'form': form, })

    def post(self, request):
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = Post(title=form.cleaned_data['title'],
                            publisher=request.user,
                            content=form.cleaned_data['content'],
                            photo=form.cleaned_data['photo'])
            new_post.save()
            return redirect('post', slug=new_post.slug)
        else:
            return render(request, 'post/post_new.html', {
                'form': form,
                'message': 'data is not valid'})


class PostDetail(LoginRequiredMixin, View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comments = Comment.objects.filter(post=post)
        comment_form = CommentForm()
        return render(request, 'post/post_detail.html', {'post': post,
                                                         'comment_form': comment_form,
                                                         'comments': comments})

    def post(self, request, slug):
        current_user = request.user
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

        if request.POST.get('delete_comment', False):
            Comment.objects.get(pk=request.GET.get('comment')).delete()

        return render(request, 'post/post_detail.html', {'post': post,
                                                         'comment_form': comment_form,
                                                         'comments': comments})


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'photo']
    template_name = 'post/post_update.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/post_delete.html'

    def get_success_url(self):
        return reverse('profile', args=[self.object.publisher.id])


class PostLikedList(LoginRequiredMixin, View):
    def get(self, request, slug):
        post_ = Post.objects.get(slug=slug)
        return render(request, 'post/post_liked_list.html', {'liked_list': post_.liked.all(),
                                                             'title': post_.title,
                                                             'slug': slug})
