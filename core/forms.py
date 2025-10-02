from django import forms


class AddPrompt(forms.Form):
    name = forms.CharField(label='название')
    text = forms.CharField(label='текст промпта')


class AddComment(forms.Form):
    text = forms.CharField(max_length=500, label='текст комментария')

