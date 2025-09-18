from django.shortcuts import render, get_object_or_404, redirect

from .models import Prompt, PromptImage
from .forms import AddPrompt

def main(request):
    """Главная страница"""

    prompts = Prompt.objects.all()

    context = {'prompts': prompts}
    return render(request, 'main.html', context)


def prompt_detail(request, prompt_id):
    """Отдельная странциа каждого промпта"""
    prompt = get_object_or_404(Prompt, id=prompt_id)

    # получаем картинки этого промпта
    images = PromptImage.objects.filter(prompt__id=prompt_id)

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