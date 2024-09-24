from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from .models import Post, Category
from django.forms import DateTimeInput

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class NewsFilter(FilterSet):
    category = ModelChoiceFilter( #создали фильтр с названием category
            field_name='postCategory',#фильтрация будет проиходить по полю postCategory
            queryset=Category.objects.all(),   #содержит значения в списке, кот б ВСЕ доступны
            label='Category',   #название поля фильтра
            empty_label='любая')#фильтрация по всем, те без фильтрации

    title = CharFilter(
            lookup_expr='iexact',
            label='Title')

    dateCreation = DateFilter(
            lookup_expr='gt', #должен применяться фильтр «больше, чем переданное значение»;
            widget=DateTimeInput({'type':'date'}), #при генерации HTML-формы требуется использовать специальный виджет.
            label='After date')

