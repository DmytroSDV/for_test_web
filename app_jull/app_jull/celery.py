import os

from celery import Celery, crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_jull.settings")

app = Celery("app_jull")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "task1": {
        "task": "utils.spiders.articles_scrape.run_spider",
        "schedule": crontab(day_of_week=1, hour=0),  # Запуск каждый понедельник в полночь
    },
    "task2": {
        "task": "news.tasks.test_func",
        "schedule": crontab(day_of_week=1, hour=0),  # Запуск каждый понедельник в полночь
    },
}
app.conf.timezone = 'UTC'