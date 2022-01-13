import celery
from os import getenv
from app.agents.scraper import Scraper

app = celery.Celery("scraper")
app.conf.update(BROKER_URL=getenv("BROKER_URL"), CELERY_RESULT_BACKEND=getenv("BROKER_URL"))


@app.task
def scraper(username, password, query, n_pages):
    results = Scraper(username, password, query, n_pages)
    return results
