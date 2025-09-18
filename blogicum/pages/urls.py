'''from django.urls import path
from django.views.generic import TemplateView

app_name = 'pages'

urlpatterns = [
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('rules/', TemplateView.as_view(template_name='pages/rules.html'), name='rules'),
]
'''
from typing import List

from django.urls import URLPattern, path

from . import views

app_name: str = "pages"

urlpatterns: List[URLPattern] = [
    path("about/", views.AboutTemplateView.as_view(), name="about"),
    path("rules/", views.RulesTemplateView.as_view(), name="rules"),
]
