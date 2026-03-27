from django import forms
from .models import Post, Comment   #Comment must be imported

#Post Form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

#Comment Form (THIS WAS MISSING)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']