from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone


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