from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class NewsForm(forms.ModelForm):
    text = forms.CharField(min_length=5) #проверка:длина текста не менее 5 символов

    class Meta:
        model = Post
        fields = [
            'author',
            # 'categoryType', убираем это поле (будем редактировать во views)
            'postCategory',
            'title',
            'text',
            'rating',
        ]

        def clean(self): #здесь можем проверить несколько полей через if
            cleaned_data = super().clean()
            title = cleaned_data.get("title")
            text = cleaned_data.get("text")

            if title == text:
                raise ValidationError(
                    "Текст новсти не должен быть идентичным заголовку."
                )
            return cleaned_data

        def clean_title(self):#здесь можем проверка конкретного поля
            title = self.cleaned_data["title"]
            if title[0].islower():
                raise ValidationError(
                    "Заголовок должен начинаться с заглавной буквы."
                )
            return title
