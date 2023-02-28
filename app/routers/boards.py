from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.board import Board
from pathlib import Path
from app.routers.auth import Auth

from app.models import mongodb
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR/"templates")

router = APIRouter(
    prefix="/boards",
    tags=["boards"],
)
title = "mydog"

validLogonCtx = Auth.validLogonCtx


@router.get("/", response_class=HTMLResponse)
async def boardPut(request: Request):

    boards = await mongodb.engine.find(Board)
    context = {"request": request, "title": title,
               "subname": "게시판", "boards": boards}

    return templates.TemplateResponse("board.html", await validLogonCtx(context, request))


@router.post("/add", response_class=HTMLResponse)
async def boardPut(request: Request, userid: str = Form(...), title: str = Form(...)):

    context = {"request": request, "title": title, "subname": "게시판"}

    if (userid is not None):
        await mongodb.engine.save(Board(title=title, userid=userid))

        return templates.TemplateResponse("board.html", await validLogonCtx(context, request))

    context["input"]
    return templates.TemplateResponse("board.html", await validLogonCtx(context, request))


# @router.post("/board/add", response_class=HTMLResponse)
# async def boardPut(request: Request, userid: str = Form(...), title: str = Form(...)):

#     await mongodb.engine.save(Board(title=title, userid=userid))
#     context = {"request": request, "title": title,
#                "subname": "게시판"}
#     # boards = await mongodb.engine.find(Board)
#     # context["boards"] = boards

#     return templates.TemplateResponse("board.html", await validLogonCtx(context, request))
