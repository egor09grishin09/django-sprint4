from django.contrib import admin

from .models import Category, Post, Location

admin.site.empty_value_display = ' - '

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Location)
