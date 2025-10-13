from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Prompt(models.Model):
    name = models.CharField(max_length=255, verbose_name='название промпта')
    text = models.TextField(verbose_name='описание промпта')
    created_at = models.DateTimeField(auto_now=True, verbose_name='дата создания')
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Промпт'
        verbose_name_plural = 'Промпты'

    def __str__(self):
        return self.name

    def likes_count(self):
        count = PromptLike.objects.filter(prompt__id=self.id).count()
        return count

    def get_hello(self):
        return 'Привет'

class PromptComment(models.Model):
    text = models.CharField(max_length=500, verbose_name='текст')
    created_at = models.DateTimeField(auto_now=True, verbose_name='дата создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, verbose_name='промпт')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class PromptImage(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, verbose_name='промпт')
    image = models.ImageField(verbose_name='картинка', upload_to='prompts')
    created_date = models.DateTimeField(auto_now=True, verbose_name='дата создания')
    class Meta:
        verbose_name = 'Картинка из промпта'
        verbose_name_plural = 'Картинки из промптов'

    def __str__(self):
        return self.prompt.name


class PromptLike(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, verbose_name='промпт', on_delete=models.CASCADE)
    created_date = models.DateTimeField(verbose_name='дата', auto_now=True)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return self.prompt.name + ' ' + self.user.username