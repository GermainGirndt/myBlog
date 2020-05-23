from django import forms
from blog.models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        # for modifing the forms css classes itself
        widgets = {
            'title': forms.TextInput(attrs={'class': 'post-title', 'placeholder': 'Title PH'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea post-content',
                                          'placeholder': 'This is the text placeholder'})
        }


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'comment-title'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea comment-content'})
        }
