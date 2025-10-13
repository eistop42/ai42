import time
import uuid

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.base import ContentFile
from django.db.models import Count

from .models import Prompt, PromptImage, PromptComment, PromptLike
from .forms import AddPrompt, AddComment
from .gen_image import generate_image

def main(request):
    """Главная страница"""

    prompts = Prompt.objects.all().order_by('-created_at')

    sort_way = request.GET.get('sort')
    if sort_way:
        if sort_way == 'name':
            prompts = prompts.order_by('name')
        elif sort_way == 'date':
            prompts = prompts.order_by('-created_at')
        elif sort_way == 'like':
            prompts = Prompt.objects.annotate(num_likes=Count('promptlike')).order_by('-num_likes')

    context = {'prompts': prompts}
    return render(request, 'main.html', context)

@login_required
def my_prompts(request):
    user = request.user

    prompts = Prompt.objects.filter(user=user).order_by('-created_at')

    context = {'prompts': prompts}
    return render(request, 'my_prompts.html', context)


def prompt_detail(request, prompt_id):
    """Отдельная странциа каждого промпта"""

    prompt = get_object_or_404(Prompt, id=prompt_id)

    add_comment = AddComment()

    # получаем картинки и комментарии этого промпта
    images = PromptImage.objects.filter(prompt__id=prompt_id).order_by('-created_date')
    comments = PromptComment.objects.filter(prompt__id=prompt_id).order_by('-created_at')
    likes_count = PromptLike.objects.filter(prompt__id=prompt_id).count()

    user = request.user

    if user.is_authenticated:
        is_liked = PromptLike.objects.filter(prompt=prompt, user=user).exists()
    else:
        is_liked = None

    context = {
        'prompt': prompt,
        'images': images,
        'comments': comments,
        'add_comment': add_comment,
        'likes_count': likes_count,
        'is_liked': is_liked
    }
    return render(request, 'prompt_detail.html', context)


@require_POST
@login_required
def delete_prompt(request, prompt_id):
    # проверить, что промпт принадлежит текущему пользователю
    user = request.user
    prompt = get_object_or_404(Prompt, id=prompt_id)

    if prompt.user == user:
        prompt.delete()
        return redirect('my_prompts')


def add_prompt(request):

    form = AddPrompt()
    user = request.user

    if request.method == 'POST' and user.is_authenticated:
        # передали данные в форму
        form = AddPrompt(request.POST)

        # проверили на валидность
        if form.is_valid():
            # достали данные
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']

            # создали объект в бд
            Prompt.objects.create(name=name, text=text, user=user)

            # перенаправляем на главную, если все ок 😎
            return redirect('/')


    context = {'form': form}

    return render(request, 'add_prompt.html', context)


@login_required
def like_prompt(request, prompt_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)
    user = request.user

    is_liked = PromptLike.objects.filter(user=user, prompt=prompt).exists()

    if is_liked:
        PromptLike.objects.filter(user=user, prompt=prompt).delete()
    else:
        PromptLike.objects.create(prompt=prompt, user=user)

    return redirect('prompt_detail', prompt_id)



def generate_image_view(request, prompt_id):

    # 1. Получить текст текущего промпта
    prompt = get_object_or_404(Prompt, id=prompt_id)
    # 2. Сходить в яндекс, получить картинку
    addition = request.POST.get('addition')
    image = generate_image(prompt.text + addition)
    # 3. Сохранить картинку в prompts
    image_file = ContentFile(image)
    # 4. Создать объект PromptImage
    prompt_image = PromptImage(prompt=prompt)
    filename = str(uuid.uuid4()) + '.jpg'
    prompt_image.image.save(filename, image_file)
    prompt_image.save()
    # 5. Перенаправить на страницу текущего промпта
    return redirect('prompt_detail', prompt.id)

@require_POST
@login_required
def add_comment(request, prompt_id):

    # передали данные в форму
    form = AddComment(request.POST)
    prompt = get_object_or_404(Prompt, id=prompt_id)

    # проверили на валидность
    if form.is_valid():
        text = form.cleaned_data.get('text')

        # достать пользователя и промпт
        user = request.user
        prompt = get_object_or_404(Prompt, id=prompt_id)

        # создать комментарий

        PromptComment.objects.create(text=text, user=user, prompt=prompt)
        return redirect('prompt_detail', prompt_id)

    # получаем картинки и комментарии этого промпта
    images = PromptImage.objects.filter(prompt__id=prompt_id).order_by('-created_date')
    comments = PromptComment.objects.filter(prompt__id=prompt_id).order_by('-created_at')

    context = {
        'prompt': prompt,
        'images': images,
        'comments': comments,
        'add_comment': form
    }
    return render(request, 'prompt_detail.html', context)

def js(request):

    if request.method == 'POST':
        time.sleep(2)
        return redirect('/js')
    return render(request, 'js.html')