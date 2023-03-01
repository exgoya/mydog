
from fastapi import APIRouter, Request, Form, exception_handlers


from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.board import Board
from app.models.sub_board import SubBoard
from app.models.comment import Comment
from pathlib import Path
from app.routers.auth import Auth
from odmantic import query, ObjectId
from app.models import mongodb
from datetime import datetime
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
async def boardAdd(request: Request, userid: str = Form(...), boardTitle: str = Form(...)):
    context = await validLogonCtx({"request": request, "title": title, "subname": "게시판"}, request)
    board = await mongodb.engine.find_one(Board, Board.title == boardTitle)

    if (board is not None):
        context["boardmsg"] = "이미 존재하는 게시판 입니다"
        context["boards"] = await mongodb.engine.find(Board)
    else:
        await mongodb.engine.save(Board(title=boardTitle, userid=userid, ts=datetime.now()))
        context["boards"] = await mongodb.engine.find(Board)
    return templates.TemplateResponse("board.html", context)


@router.post("/delete", response_class=HTMLResponse)
async def boardDelete(request: Request, boardId: list[ObjectId] = Form(...)):
    print(boardId)

    # remove board
    delcnt = await mongodb.engine.remove(Board, query.in_(Board.id, boardId))

    # remove subBoard
    print(await mongodb.engine.remove(SubBoard, query.in_(SubBoard.boardId, boardId)))

    # remove comment
    print(await mongodb.engine.remove(Comment, query.in_(Comment.boardId, boardId)))

    context = await validLogonCtx({"request": request, "title": title, "subname": "게시판"}, request)
    context["boards"] = await mongodb.engine.find(Board)
    context["boardmsg"] = str(delcnt) + "개 삭제 되었습니다"
    return templates.TemplateResponse("board.html", context)
