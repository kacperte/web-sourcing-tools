from celery import Celery
import os
from app.agents.scraper import Scraper

app = Celery("scraper")
app.conf.update(
    BROKER_URL=os.environ.get(["REDIS_URL"], CELERY_RESULT_BACKEND=os.environ.get["REDIS_URL"])
)


@app.task()
def scraper(username, password, query, n_pages):
    results = Scraper(username, password, query, n_pages)
    return results
