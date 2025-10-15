from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone


User = get_user_model()


class PostManager(models.Manager):
    def post_all_query(self):
        """Возвращает все посты."""
        return self.get_queryset().select_related(
            "category",
            "location",
            "author"
        ).annotate(
            comment_count=models.Count("comments")
        ).order_by("-pub_date")

    def post_published_query(self):
        """Возвращает опубликованные посты."""
        return self.post_all_query().filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )

    def get_post_data(self, pk):
        """Возвращает данные поста."""
        return get_object_or_404(self.post_all_query(), pk=pk)


class BaseModel(models.Model):
    """
    Абстрактная модель.
    Добавляет к модели дату создания и флаг "опубликовано".
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    """Категория."""

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ("title",)

    def __str__(self):
        return self.title


class Location(BaseModel):
    """Местоположение."""

    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ("name",)

    def __str__(self):
        return self.name


class Post(BaseModel):
    """Пост."""

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    image = models.ImageField(
        upload_to="images/",
        verbose_name='Изображение',
        blank=True,
    )

    objects = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = "posts"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Comment(BaseModel):
    """Комментарий."""

    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Комментируемый пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено",
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = "comments"
        ordering = ('created_at',)

    def __str__(self):
        return self.text[:30]

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post.pk})
