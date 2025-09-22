from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.base import ContentFile
import uuid

from .models import Prompt, PromptImage
from .forms import AddPrompt
from .gen_image import generate_image

def main(request):
    """Главная страница"""

    prompts = Prompt.objects.all()

    context = {'prompts': prompts}
    return render(request, 'main.html', context)


def prompt_detail(request, prompt_id):
    """Отдельная странциа каждого промпта"""
    prompt = get_object_or_404(Prompt, id=prompt_id)

    # получаем картинки этого промпта
    images = PromptImage.objects.filter(prompt__id=prompt_id).order_by('-created_date')

    context = {'prompt': prompt, 'images': images}
    return render(request, 'prompt_detail.html', context)


def add_prompt(request):

    form = AddPrompt()

    if request.method == 'POST':
        # передали данные в форму
        form = AddPrompt(request.POST)

        # проверили на валидность
        if form.is_valid():
            # достали данные
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']

            # создали объект в бд
            Prompt.objects.create(name=name, text=text)

            # перенаправляем на главную, если все ок 😎
            return redirect('/')


    context = {'form': form}

    return render(request, 'add_prompt.html', context)


def generate_image_view(request, prompt_id):

    # 1. Получить текст текущего промпта
    prompt = get_object_or_404(Prompt, id=prompt_id)
    # 2. Сходить в яндекс, получить картинку
    image = generate_image(prompt.text)
    # 3. Сохранить картинку в prompts
    image_file = ContentFile(image)
    # 4. Создать объект PromptImage
    prompt_image = PromptImage(prompt=prompt)
    filename = str(uuid.uuid4()) + '.jpg'
    prompt_image.image.save(filename, image_file)
    prompt_image.save()
    # 5. Перенаправить на страницу текущего промпта
    return redirect('prompt_detail', prompt.id)

