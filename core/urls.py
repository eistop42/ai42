from django.urls import path

from .views import *

urlpatterns = [
    path('', main),
    path('prompts/<int:prompt_id>', prompt_detail, name='prompt_detail'),
    path('prompts/add', add_prompt, name='add_prompt')
]