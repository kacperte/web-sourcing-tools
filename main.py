from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from app.library.helpers import *
from app.agents.string_builder import string_builder
from tasks import scraper


LOGIN = os.environ.get("LOGIN")
PASS = os.environ.get("PASS")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.post("/common-words")
def form_post(
    request: Request,
    string_or: str = Form(...),
    string_and: str = Form(...),
    string_not: str = Form(...),
):
    query = string_builder(OR=string_or, AND=string_and, NOT=string_not)
    n_page = 2
    task = scraper.delay(LOGIN, PASS, query, n_page)
    return templates.TemplateResponse(
        "form.html", context={"request": request, "result": 'test'}
    )


@app.get("/common-words")
def form_post(request: Request):

    result = ""
    return templates.TemplateResponse(
        "form.html", context={"request": request, "result": result}
    )


if __name__ == "__main__":
    app.run()
