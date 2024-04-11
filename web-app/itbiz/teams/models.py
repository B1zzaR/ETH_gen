from django.db import models


class Articles(models.Model):
    title = models.CharField('Название', max_length=30)
    anons = models.CharField('Анонс', max_length=100)
    full_text = models.TextField('Статья')

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'