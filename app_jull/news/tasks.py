from app_jull.celery import app


@app.task
def test_func():
    return "tests"
