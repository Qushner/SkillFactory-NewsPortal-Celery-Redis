from django.urls import path
# Импортируем созданное нами представление
from .views import (NewsList, NewsDetail, NewsSearch, NewsCreate, NewsUpdate, NewsDelete, subscriptions)


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
   path('search/', NewsSearch.as_view(), name='news_search'),

   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('article/create/', NewsCreate.as_view(), name='article_create'),

   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('article/<int:pk>/update/', NewsUpdate.as_view(), name='article_update'),


   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('article/<int:pk>/delete/', NewsDelete.as_view(), name='article_delete'),

   path('subscriptions/', subscriptions, name='subscriptions'),
]
