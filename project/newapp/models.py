from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete = models.CASCADE)# cвязь «один к одному» с встроенной моделью пользователей User;
    ratingAuthor = models.SmallIntegerField(default = 0)# рейтинг пользователя
    def __str__(self):
        return self.authorUser.username
# Метод update_rating() модели Author, который обновляет рейтинг текущего автора
    # (метод принимает в качестве аргумента только self).
# Он состоит из следующего:
# суммарный рейтинг каждой статьи автора умножается на 3;
# суммарный рейтинг всех комментариев автора;
# суммарный рейтинг всех комментариев к статьям автора.
    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))# к связанной модели Post применяем функцию agregate,
        #которая применяет функцияю Sum к rating (в Post есть rating).
        #и он суммирует все значения rating у модели Post, связанные с этим Автором
        # итого вычислили, но не получили
        pRat = 0
        pRat += postRat.get('postRating') or 0 #получаем значение суммарного рейтинга каждой статьи автора

        commentRat = self.authorUser.comment_set.aggregate(commentRating = Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating') or 0 # получаем значение суммарного рейтинга всех комментариев автора;

        self.ratingAuthor = pRat*3 + cRat
        self.save()


class Category(models.Model): #категории новостей/статей — темы, которые они отражают
    name = models.CharField(max_length = 64, unique = True)# Поле должно быть уникальным
    # subscribers = models.ManyToManyField(User, related_name='categories') #поле подписчиков users.categories.all()
    # #один польз-ль мб подписан на неск категорий и наоборот
    # # related_name='categories' - через него обращаться ко всем категориям пользователя через объект поль-ля : users.calegories.all()
    def __str__(self): #__str__() – магический метод для отображения информации об объекте класса для пользователей
        return self.name


class Post(models.Model):# содержать в себе статьи и новости, которые создают пользователи
    author = models.ForeignKey(Author, on_delete = models.CASCADE)# связь «один ко многим» с моделью Author;
    News = 'NW'# новость
    Article = 'AR'# статья
    CATEGORY_CHOICES = (
        (News, 'Новость'),
        (Article, 'Статья')
    )
    categoryType = models.CharField(max_length = 2, choices = CATEGORY_CHOICES, default = Article)# поле с выбором — «статья» или «новость»;
    dateCreation = models.DateTimeField(auto_now_add = True)# автоматически добавляемая дата и время создания;
    postCategory = models.ManyToManyField(Category, through= 'PostCategory')# связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    title = models.CharField(max_length= 128) # заголовок статьи/новости;
    text = models.TextField() # текст статьи/новости;
    rating = models.SmallIntegerField(default=0)# рейтинг статьи/новости.

    def like(self):#увеличивают рейтинг на единицу
        self.rating += 1 #определенный объект поля rating += 1
        self.save() #встроенный метод для сохранения изменений

    def dislike(self):#уменьшают рейтинг на единицу
        self.rating -= 1  # определенный объект поля rating -= 1
        self.save()  # встроенный метод для сохранения изменений

    def preview(self):
       return self.text[:123] + "..." #возвращает начало статьи (предварительный просмотр) длиной 124 символа

    def __str__(self):
        return f'{self.title} : {self.dateCreation} : {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])
class PostCategory(models.Model):# Промежуточная модель для связи «многие ко многим»:
    postThrought = models.ForeignKey(Post, on_delete = models.CASCADE)# связь «один ко многим» с моделью Post;
    categoryThrought = models.ForeignKey(Category, on_delete = models.CASCADE)# связь «один ко многим» с моделью Category.
    pass


class Comment(models.Model):# Под каждой новостью/статьёй можно оставлять комментарии: cпособ хранения
    commentPost = models.ForeignKey(Post, on_delete = models.CASCADE)# связь «один ко многим» с моделью Post;
    commentUser = models.ForeignKey(User, on_delete = models.CASCADE)# связь «один ко многим» со встроенной моделью User
    text = models.TextField ()# текст комментария;
    dateCreation = models.DateTimeField(auto_now_add = True)# дата и время создания комментария;
    rating = models.SmallIntegerField(default=0)# рейтинг комментария.

    def like(self):  # увеличивают рейтинг на единицу
        self.rating += 1  # определенный объект поля rating += 1
        self.save()  # встроенный метод для сохранения изменений

    def dislike(self):  # уменьшают рейтинг на единицу
        self.rating -= 1  # определенный объект поля rating -= 1
        self.save()  # встроенный метод для сохранения изменений


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )





