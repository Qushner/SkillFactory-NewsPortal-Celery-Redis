from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),

   # Делаем так, чтобы все адреса из нашего приложения (newapp/urls.py)
   # подключались к главному приложению с префиксом news/.
   path('news/', include('newapp.urls')),

   # #Django скажет, как обрабатывать запросы от пользователей по ссылкам, которые начинаются с /accounts/
   # path('accounts/', include('django.contrib.auth.urls')),
   #
   # path("accounts/", include("accounts.urls")),  # Добавили эту строчку
   path("accounts/", include("allauth.urls"))

   ]
