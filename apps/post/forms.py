from django import forms
from django.core.exceptions import ValidationError

from apps.post.models import *


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'photo']

    def clean(self):
        cleaned_data = super().clean()
        content, photo = cleaned_data['content'], cleaned_data['photo']
        if not content and not photo:
            raise ValidationError('You need to add text or photo as content.')


class CommentForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200)
    content = forms.CharField(label='content', widget=forms.Textarea)
