from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.core.exceptions import PermissionDenied

from .forms import CustomUserCreationForm, EditUserProfileForm

User = get_user_model()


class UserCreateView(CreateView):
    template_name = "registration/registration_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("blog:index")


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditUserProfileForm
    template_name = "blog/user.html"
    
    # Убираем success_url и обрабатываем успех вручную
    success_url = None

    def get_object(self):
        username = self.kwargs.get('username')
        if username != self.request.user.username:
            raise PermissionDenied("Вы не можете редактировать чужой профиль")
        return self.request.user

    def form_valid(self, form):
        form.save()
        # Возвращаем тот же шаблон с сообщением об успехе (статус 200)
        return self.render_to_response(
            self.get_context_data(form=form, success=True)
        )
    