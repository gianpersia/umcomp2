from celery import Celery

app = Celery('calcmatriz', broker='redis://localhost:6379', backend='redis://localhost:6379', include=['calcmatriz'])