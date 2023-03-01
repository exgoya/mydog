
from fastapi import APIRouter, Request, Form

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.sub_board import SubBoard
from pathlib import Path
from app.routers.auth import Auth
from app.models import mongodb
from datetime import datetime
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR/"templates")

router = APIRouter(
    prefix="/boards/sub",
    tags=["sub_boards"],
)
title = "mydog"

validLogonCtx = Auth.validLogonCtx


@router.get("/{boardTitle}", response_class=HTMLResponse)
async def subBoard(request: Request, boardTitle: str, boardId: str):
    context = await validLogonCtx({"request": request, "title": title, "subname": boardTitle + " 게시판", "boardTitle": boardTitle}, request)

    sboard = await mongodb.engine.find(SubBoard, SubBoard.boardId == boardId)

    if (sboard is not None):
        context["subBoards"] = sboard
        context["boardId"] = boardId
    return templates.TemplateResponse("sub_board.html", context)


@router.post("/add", response_class=HTMLResponse)
async def boardAdd(request: Request, userid: str = Form(...), boardTitle: str = Form(...), sub_title: str = Form(...), sub_desc: str = Form(...), boardId: str = Form(...)):

    context = await validLogonCtx({"request": request, "title": title, "subname": boardTitle + " 게시판", "boardTitle": boardTitle}, request)

    await mongodb.engine.save(SubBoard(title=sub_title, desc=sub_desc, userid=userid, boardId=boardId, cts=datetime.now(), uts=datetime.now()))
    subBoard = await mongodb.engine.find(SubBoard, SubBoard.boardId == boardId)
    context["subBoards"] = subBoard
    context["boardId"] = boardId
    return templates.TemplateResponse("sub_board.html", context)
