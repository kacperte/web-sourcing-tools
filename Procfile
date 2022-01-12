web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
worker: celery worker --app=tasks.app