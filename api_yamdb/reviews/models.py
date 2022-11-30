from django.db import models


class Title(models.Model):
    pass


class Review(models.Model):
    author = models.IntegerField()  # Временно
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.IntegerField()
    text = models.TextField()
    title = models.IntegerField()  # Временно

    def __str__(self):
        return self.text
