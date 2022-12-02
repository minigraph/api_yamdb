from django.contrib import admin
from .models import Review, Title, Category, Comment


admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Comment)
