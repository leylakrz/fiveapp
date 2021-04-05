from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from django.views.generic.base import View

from apps.event.models import *
from apps.post.forms import *


class NewPostView(LoginRequiredMixin, View):
    """
    each member can publish a new post.
    if publish is successful, member is redirected to the post.
    """

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
    """
    returns post's detail and comments published for this post.
    publisher can edit or delete the post.
    each visitor other than publisher can like the post or unlike (take back their like) it.
    each member can publish a new comment and delete only their own comment.
    """
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comments = Comment.objects.filter(post=post)
        comment_form = CommentForm()
        return render(request, 'post/post_detail.html', {'post': post,
                                                         'comment_form': comment_form,
                                                         'comments': comments})

    def post(self, request, slug):
        current_user = request.user
        current_post = Post.objects.get(slug=slug)

        # like
        if request.POST.get('like', False):
            if current_user not in current_post.liked.all():
                current_post.liked.add(current_user)
                current_post.save()
                # new event object will inform the post's publisher their post is liked.
                Event(operator=request.user, viewer=current_post.publisher, type='like',
                      foreign_key=current_post.id).save()

        if request.POST.get('unlike', False):
            if current_user in current_post.liked.all():
                current_post.liked.remove(current_user)
                current_post.save()

                Event.objects.filter(operator=request.user, viewer=current_post.publisher, type='like',
                                     foreign_key=current_post.id).delete()

        # comment
        comment_form = CommentForm(request.POST)
        if request.POST.get('comment', False):
            current_comment = Comment(publisher=current_user,
                                      post=current_post,
                                      title=request.POST['title'],
                                      content=request.POST['content'],
                                      )
            current_comment.save()

            # new event object will inform the post's publisher someone has published a comment for their post.
            Event(operator=request.user, viewer=current_comment.post.publisher, type='comment',
                  foreign_key=current_comment.id).save()

            comment_form = CommentForm()
        comments = Comment.objects.filter(post=current_post)

        if request.POST.get('delete_comment', False):
            current_comment = Comment.objects.get(pk=request.GET.get('comment'))
            Event.objects.filter(operator=request.user, viewer=current_comment.post.publisher, type='comment',
                                 foreign_key=current_comment.id).delete()

            current_comment.delete()

        # end
        return render(request, 'post/post_detail.html', {'post': current_post,
                                                         'comment_form': comment_form,
                                                         'comments': comments})


class PostUpdate(LoginRequiredMixin, UpdateView):
    """
    a member can update their post.
    after updating, member will be redirected to the post.
    """
    model = Post
    fields = ['title', 'content', 'photo']
    template_name = 'post/post_update.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    """
    a member can delete their post.
    after deleting, member will be redirected to their profile.
    """
    model = Post
    template_name = 'post/post_delete.html'

    def get_success_url(self):
        return reverse('profile', args=[self.object.publisher.id])


class PostLikedList(LoginRequiredMixin, View):
    """
    returns list of members liked a certain post.
    """

    def get(self, request, slug):
        current_post = Post.objects.get(slug=slug)
        return render(request, 'post/post_liked_list.html', {'liked_list': current_post.liked.all(),
                                                             'title': current_post.title,
                                                             'slug': slug})
