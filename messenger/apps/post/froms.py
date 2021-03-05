from django import forms

from apps.post.models import *


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200)
    content = forms.CharField(label='content', widget=forms.Textarea)
