from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from blog.models import Comment, Post


User = get_user_model()


class CommentMixinView(View):
    """Миксин для редактирования и удаления комментария."""

    model = Comment
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_pk"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect("blog:post_detail", pk=self.kwargs["pk"])
        Post.objects.get_post_data(self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("blog:post_detail", kwargs={"pk": pk})


class PostQuerySetMixin:
    author = None
    post_data = None

    def get_author(self):
        """Получение объекта автора по username из URL, если доступен."""
        if self.author is None:
            username = self.kwargs.get("username")
            if username:
                self.author = get_object_or_404(User, username=username)
            else:
                self.author = self.request.user
        return self.author

    def get_post_data(self):
        """Получение данных поста по pk."""
        if self.post_data is None:
            pk = self.kwargs.get('pk')
            if pk:
                self.post_data = get_object_or_404(Post, pk=pk)
        return self.post_data

    def get_queryset(self):
        """Получение queryset для постов."""
        author = self.get_author()
        post_data = self.get_post_data()

        if post_data:
            if post_data.author == self.request.user:
                return Post.objects.post_all_query().filter(pk=post_data.pk)
            return Post.objects.post_published_query().filter(
                    pk=post_data.pk
                )
        else:
            if author == self.request.user:
                return Post.objects.post_all_query().filter(author=author)
            return Post.objects.post_published_query().filter(
                    author=author
                )


class NotAuthorRedirectMixin:

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect("blog:post_detail", pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)
