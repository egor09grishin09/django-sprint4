from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    # Главная страница.
    path(
        '',
        views.MainPostsListView.as_view(),
        name='index'
    ),
    # Страница определенной категории.
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostListView.as_view(),
        name='category_posts'
    ),
    # Страница профиля пользователя с его публикациями.
    path(
        'profile/<slug:username>/',
        views.UserProfileListView.as_view(),
        name='profile'
    ),
    # Страница редактирования данных профиля пользователя.
    path(
        'edit_profile/',
        views.UserProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    # Страница поста.
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    # Страница создания поста.
    path(
        'posts/create/',
        views.PostCreateView.as_view(),
        name='create_post'
    ),
    # Страница редактирования поста.
    path(
        'posts/<int:pk>/edit/',
        views.EditPostView.as_view(),
        name='edit_post',
    ),
    # Страница удаления поста.
    path(
        'posts/<int:pk>/delete/',
        views.DeletePostView.as_view(),
        name='delete_post',
    ),
    # Добавление комментария.
    path(
        'posts/<int:pk>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'
    ),
    # Редактирование комментария.
    path(
        'posts/<int:pk>/edit_comment/<int:comment_pk>/',
        views.EditCommentView.as_view(),
        name='edit_comment',
    ),
    # Удаление комментария.
    path(
        'posts/<int:pk>/delete_comment/<int:comment_pk>/',
        views.DeleteCommentView.as_view(),
        name='delete_comment',
    ),
]
