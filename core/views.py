from django.shortcuts import render, get_object_or_404

from .models import Prompt

def main(request):
    """Главная страница"""

    prompts = Prompt.objects.all()

    context = {'prompts': prompts}
    return render(request, 'main.html', context)


def prompt_detail(request, prompt_id):
    """Отдельная странциа каждого промпта"""
    prompt = get_object_or_404(Prompt, id=prompt_id)

    context = {'prompt': prompt}
    return render(request, 'prompt_detail.html', context)