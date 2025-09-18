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


class PromptImage(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, verbose_name='промпт')
    image = models.ImageField(verbose_name='картинка', upload_to='prompts')
    created_date = models.DateTimeField(auto_now=True, verbose_name='дата создания')
    class Meta:
        verbose_name = 'Картинка из промпта'
        verbose_name_plural = 'Картинки из промптов'

    def __str__(self):
        return self.prompt.name