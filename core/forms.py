from django import forms


class AddPrompt(forms.Form):
    name = forms.CharField(label='название')
    text = forms.CharField(label='текст промпта')

