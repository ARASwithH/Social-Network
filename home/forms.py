from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Title', }),
            'content': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Content', }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', ]
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Write your Comment...', }),
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', ]

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Write your reply...',
                                             'rows': 2, })}

