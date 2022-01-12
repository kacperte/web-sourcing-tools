import celery
from os import getenv

app = celery.Celery("scraper")
app.conf.update(BROKER_URL=getenv('BROKER_URL'))


@app.task
def scraper(function, username, password, query, n_pages):
    results = function(username, password, query, n_pages)
    return results

