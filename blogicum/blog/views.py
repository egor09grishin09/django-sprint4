from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import CommentForm, PostForm, UserEditForm
from blog.models import Category, Comment, Post, User
from constants import PAGINATION_QTY
from core.mixins import (
    CommentMixinView,
    NotAuthorRedirectMixin,
    PostQuerySetMixin,
)


class MainPostsListView(ListView):
    """Главная страница с постами."""

    model = Post
    template_name = 'blog/index.html'
    queryset = Post.objects.post_published_query()
    paginate_by = PAGINATION_QTY


class CategoryPostListView(MainPostsListView):
    """Страница со списком постов выбранной категории."""

    template_name = "blog/category.html"
    category = None

    def get_queryset(self):
        slug = self.kwargs["category_slug"]
        self.category = get_object_or_404(
            Category, slug=slug, is_published=True
        )
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class UserProfileListView(PostQuerySetMixin, ListView):
    """Страница с информацией о пользователе и списком его публикаций."""

    template_name = "blog/profile.html"
    paginate_by = PAGINATION_QTY

    def get_context_data(self, **kwargs):
        """Добавление данных о профиле в контекст."""
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_author()
        return context


class PostDetailView(PostQuerySetMixin, DetailView):
    """Страница выбранного поста."""

    model = Post
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flag"] = True
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.all().select_related(
            "author"
        )
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление профиля пользователя."""

    template_name = "blog/user.html"
    model = User
    form_class = UserEditForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        username = self.get_object()
        return reverse("blog:profile", kwargs={"username": username})


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание поста."""

    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user
        return reverse("blog:profile", kwargs={"username": username})


class EditPostView(LoginRequiredMixin, NotAuthorRedirectMixin, UpdateView):
    """Редактирование поста."""

    model = Post
    form_class = PostForm
    template_name = "blog/create.html"


class DeletePostView(LoginRequiredMixin, NotAuthorRedirectMixin, DeleteView):
    """Удаление поста."""

    model = Post
    template_name = "blog/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        username = self.request.user
        return reverse("blog:profile", kwargs={"username": username})


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария."""

    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = Post.objects.get_post_data(self.kwargs['pk'])
        if not post:
            raise Http404("Post not found")
            
        form.instance.post = post
        if post.author != self.request.user:
            self.send_author_email(post)
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("blog:post_detail", kwargs={"pk": pk})

    def send_author_email(self, post):
        post_url = self.request.build_absolute_uri(self.get_success_url())
        recipient_email = post.author.email
        subject = "New comment"
        message = (
            f"Пользователь {self.request.user} добавил "
            f"комментарий к посту {post.title}.\n"
            f"Читать комментарий {post_url}"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_FROM,
            recipient_list=[recipient_email],
            fail_silently=True,
        )


class EditCommentView(CommentMixinView, UpdateView):
    """Редактирование комментария."""

    form_class = CommentForm


class DeleteCommentView(CommentMixinView, DeleteView):
    """Удаление комментария."""
