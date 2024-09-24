import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.utils import timezone

from newapp.models import Post, Subscription

logger = logging.getLogger(__name__)


def my_job():# Your job processing logic here...
    today = timezone.now() #определяем текущее время (в таблице время с часовым поясом. ошибка "наивное время")
    last_week = today - datetime.timedelta(days=7)#первоначальная точка отсчета для рассылки появившихся новостей
    posts = Post.objects.filter(dateCreation__gte=last_week)#фильтруем созданные новости за период позднее (>=) чем 7 дней назад. dateCreation из Post

    # все категории статей в виде списка (а не словаря тк flat=True)(по названию категории, а не по id)
    categories = set(posts.values_list('postCategory__name', flat=True))#set множество для уникальности значений

    # все подписчики категорий (имя категорий совпадает с categories)  статей в виде списка email (а не словаря тк flat=True)(по названию категории, а не по id СМ ВЫШЕ)
    subscribers = set(Subscription.objects.filter(category__name__in=categories).values_list('user__email', flat=True))

    html_content = render_to_string('daily_post.html',
                                    {'link': settings.SITE_URL,
                                     'posts': posts})#в цикле б проходиться и добавлять в шаблон
    msg = EmailMultiAlternatives(
        subject="Статьи за неделю",
        body='',#пустой тк шаблон есть
        from_email=settings.DEFAULT_FROM_EMAIL,#из settings
        to=subscribers)

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),  # команда запускается
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="fri", hour="17", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")