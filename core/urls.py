from django.urls import path

from .views import *

urlpatterns = [
    path('', main),
    path('prompts/<int:prompt_id>', prompt_detail, name='prompt_detail'),
    path('prompts/<int:prompt_id>/generate', generate_image_view, name='generate_image'),
    path('prompts/add', add_prompt, name='add_prompt'),
    path('prompts/my', my_prompts, name='my_prompts')
]