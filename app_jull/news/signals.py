
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from utils.spiders.articles_scrape import run_spider
from news.tasks import test_func

@receiver(post_migrate, sender=AppConfig)
def run_initial_tasks(sender, **kwargs):
    # Запуск задач после миграции базы данных (старте приложения)
    run_spider.delay()  # Запуск задачи из модуля utils.spiders.articles_scrape
    test_func.delay()    # Запуск задачи из модуля news.tasks