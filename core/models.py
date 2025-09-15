from django.db import models

class Prompt(models.Model):
    name = models.CharField(max_length=255, verbose_name='название промпта')
    text = models.TextField(verbose_name='описание промпта')
    created_at = models.DateTimeField(auto_now=True, verbose_name='дата создания')

    class Meta:
        verbose_name = 'Промпт'
        verbose_name_plural = 'Промпты'

    def __str__(self):
        return self.name
