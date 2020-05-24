from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView,
                                  )
# Create your views here.


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = Post

    # django ORM when dealing with generic views -> custom touch
    # thats a sql query: grab the post object and filter based on this condition
    # lte => less than or equal to
    # translates to 'SELECT * FROM Post where published_date <= timezone.now...;'
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    # Mixin for loggin required
    login_url = '/login/'
    # After post creation
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    # Mixin for loggin required
    login_url = '/login/'
    # After post creation
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Post

    def get_success_url(self):
        obj = self.get_object()
        if obj.published_date:
            return reverse_lazy('post_list')
        else:
            return reverse_lazy('post_draft_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'blog/post_draft_list.html'
    model = Post

    def get_queryset(self):
        # isnull because drafts are not yet published
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


##############################################
##############################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    # Post model already imported
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # because of the comment.post attribute is linked to the FK
            comment.post = post
            comment.save()
            # post.pk = local pk
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # method of Comment that setts approved_comment to True
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
