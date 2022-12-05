from django.contrib import admin

from .models import (
    Category,
    Comment,
    Review,
    Title,
    Genre,
    GenresOfTitles
)

admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(GenresOfTitles)
