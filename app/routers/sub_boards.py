
from fastapi import APIRouter, Request, Form

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.board import Board, SubBoard
from pathlib import Path
from app.routers.auth import Auth
from odmantic import query
from app.models import mongodb
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR/"templates")

router = APIRouter(
    prefix="/boards/sub",
    tags=["sub_boards"],
)
title = "mydog"

validLogonCtx = Auth.validLogonCtx


@router.get("/{boardTitle}", response_class=HTMLResponse)
async def subBoard(request: Request, boardTitle: str):
    context = await validLogonCtx({"request": request, "title": title, "subname": boardTitle + " 게시판", "boardTitle": boardTitle}, request)

    board = await mongodb.engine.find_one(Board, Board.title == boardTitle)
    if (board.subBoards is not None):
        context["subBoards"] = board.subBoards
    return templates.TemplateResponse("sub_board.html", context)


@router.post("/add", response_class=HTMLResponse)
async def boardAdd(request: Request, userid: str = Form(...), boardTitle: str = Form(...), sub_title: str = Form(...), sub_desc: str = Form(...)):

    context = await validLogonCtx({"request": request, "title": title, "subname": boardTitle + " 게시판", "boardTitle": boardTitle}, request)

    board = await mongodb.engine.find_one(Board, Board.title == boardTitle)
    if (board.subBoards is None):
        board.subBoards = [
            SubBoard(title=sub_title, desc=sub_desc, userid=userid)]
    else:
        board.subBoards.append(
            SubBoard(title=sub_title, desc=sub_desc, userid=userid))

    await mongodb.engine.save(board)
    context["subBoards"] = board.subBoards
    return templates.TemplateResponse("sub_board.html", context)


# @router.post("/add", response_class=HTMLResponse)
# async def boardAdd(request: Request, userid: str = Form(...), boardTitle: str = Form(...)):
#     context = await validLogonCtx({"request": request, "title": title, "subname": "게시판"}, request)
#     board = await mongodb.engine.find_one(Board, Board.title == boardTitle)

#     if (board is not None):
#         context["boardmsg"] = "이미 존재하는 게시판 입니다"
#         context["boards"] = await mongodb.engine.find(Board)
#     else:
#         await mongodb.engine.save(Board(title=boardTitle, userid=userid))
#         context["boards"] = await mongodb.engine.find(Board)
#     return templates.TemplateResponse("board.html", context)
