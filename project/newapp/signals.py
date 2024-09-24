# from django.conf import settings
# from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from django.template.defaultfilters import truncatechars
#
# from .models import PostCategory #Промежуточная модель для связи «многие ко многим» между Post и Category
#
#
# @receiver(m2m_changed, sender=PostCategory) #receiver использует сигнал m2m, который срабатывает после сохранения конкретной модели в базе данных.
# def post_created(instance, **kwargs):
#     if kwargs['action'] != 'post_add': #"post_add" - сигнал отправляется после добавления в отношение одного или нескольких объектов
#         return #здесь не отправляется, тк !=
#
#     # instance - объект модели, где есть поле MtM (те post), кот изменяется при создании поста и кот связано с sender-ом
#     emails = User.objects.filter(
#         subscriptions__category__in=instance.postCategory.all() #применяем поле MtM к instance, чтобы получить связанные с ним объекты модели Category
#         #all() - тк ссылка на список связанных объектор модели PostCategory
#     ).values_list('email', flat=True)
#
#     subject = f'Another news has appeared which is concerned with {",".join(category.name for category in instance.postCategory.all())} category' #list comprehension («генератора списка»)
#
#     text_content = (
#         f'Title: {instance.title}\n'
#         f'Text: {instance.preview()}\n\n'
#         f'Url: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Title: {instance.title}<br>'
#         f'Text: {instance.preview()}<br><br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Url</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()