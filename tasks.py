from celery import Celery
import os
from app.agents.scraper import Scraper

app = Celery(__name__)
app.conf.update(
    BROKER_URL=os.environ["REDIS_URL"],
    CELERY_RESULT_BACKEND=os.environ["REDIS_URL"]
)


@app.task(name="scraper")
def scraper(username, password, query, n_pages):
    results = Scraper(username, password, query, n_pages)
    return results


