from django import forms
from blog.models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        # for modifing the forms css classes itself
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-post-title', 'placeholder': 'Enter post title'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea form-post-content',
                                          'placeholder': 'Enter post text'})
        }


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-comment-title', 'placeholder': 'Enter author name'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea form-comment-content', 'placeholder':'Enter comment'})
        }
