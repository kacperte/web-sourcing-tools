from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from os import getenv
from dotenv import load_dotenv
from .agents.scraper import Scraper


q = r"site:linkedin.com/in/ OR site:linkedin.com/pub/ Warszawa (Angular OR React) -Manager -Lider"
n = 2
load_dotenv()
LOGIN = getenv('LOGIN')
PASS = getenv('PASS')

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        "page": "Home page"
    }
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/scrap")
async def scrap():
    scraper = Scraper(username=LOGIN,
                      password=PASS,
                      query=q,
                      n_pages=n,
                      )
    return scraper.talent_mapping()
