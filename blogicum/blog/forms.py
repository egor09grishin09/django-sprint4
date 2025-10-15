from django.forms import DateTimeInput, ModelForm, Textarea
from django.utils import timezone

from .models import Comment, Post, User


class UserEditForm(ModelForm):
    """Форма редактирования информации о пользователе."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")


class CommentForm(ModelForm):
    """Форма комментария."""

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            "text": Textarea({"rows": "3"})
        }


class PostForm(ModelForm):
    """Форма поста."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()
        ).strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}
            )
        }
