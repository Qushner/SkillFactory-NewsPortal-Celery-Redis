#импортируем библиотеку для взаимодействия с операционной системой и саму библиотеку Celery
import os
from celery import Celery
from celery.schedules import crontab

#cвязываем настройки Django с настройками Celery через переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации.
app = Celery('project')
#указываем пространство имен, чтобы Celery сам находил все необходимые настройки
#в общем конфигурационном файле settings.py. Он их будет искать по шаблону «CELERY_***».
app.config_from_object('django.conf:settings', namespace='CELERY')
# указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта.
app.autodiscover_tasks()



# чтобы выполнить какую-то задачу каждый понедельник в 8 утра, необходимо в расписание добавить следующее:
app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'newapp.tasks.weekly_send_email_task',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}