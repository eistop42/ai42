from django import forms


class AddPrompt(forms.Form):
    name = forms.CharField(label='название')
    text = forms.CharField(label='текст промпта')


class AddComment(forms.Form):
    text = forms.CharField(max_length=500, label='текст комментария')

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if 'дурак' in text:
            raise forms.ValidationError('Некорректный комментарий')
        return text

