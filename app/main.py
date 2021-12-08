from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from os import getenv
import pandas as pd
from dotenv import load_dotenv
from .agents.scraper import Scraper
from .library.helpers import *
from .agents.string_builder import string_builder


n = 2
load_dotenv()
LOGIN = getenv('LOGIN')
PASS = getenv('PASS')

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

"""
@app.get("/common-words")
def common(request: Request):
    result = scraper.talent_mapping()
    return templates.TemplateResponse('page.html', context={'request': request, 'data': result})
"""


@app.get("/common-words")
def form_post(request: Request):

    result = ""
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.post("/common-words")
async def form_post(request: Request,
                    string_or: str = Form(...),
                    string_and: str = Form(...),
                    string_not: str = Form(...)):

    query = string_builder(OR=string_or, AND=string_and, NOT=string_not)
    n_page = 10
    scraper = Scraper(username=LOGIN,
                      password=PASS,
                      query=query,
                      n_pages=n_page,
                      )
    result = scraper.talent_mapping()
    result_df = pd.DataFrame({"word": result.values(), "quantity": result.keys()})

    return templates.TemplateResponse("form.html", context={"request": request, "result": result})
