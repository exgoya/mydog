
from fastapi import APIRouter, Request, Form
from odmantic import ObjectId, query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.sub_board import SubBoard
from app.models.board import Board
from app.models.comment import Comment
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


@router.get("/{boardId}", response_class=HTMLResponse)
async def subBoard(request: Request, boardId: ObjectId):

    sboard = await mongodb.engine.find(SubBoard, SubBoard.boardId == boardId)
    board = await mongodb.engine.find_one(Board, Board.id == boardId)

    context = await validLogonCtx({"request": request, "title": title, "subname": board.title + " 게시판", "boardTitle": board.title}, request)

    if (sboard is not None):
        context["subBoards"] = sboard
        context["boardId"] = boardId
    return templates.TemplateResponse("sub_board.html", context)


@router.post("/add", response_class=HTMLResponse)
async def boardAdd(request: Request, userid: str = Form(...), boardTitle: str = Form(...), sub_title: str = Form(...), sub_desc: str = Form(...), boardId: ObjectId = Form(...)):

    context = await validLogonCtx({"request": request, "title": title, "subname": boardTitle + " 게시판", "boardTitle": boardTitle}, request)

    await mongodb.engine.save(SubBoard(title=sub_title, desc=sub_desc, userid=userid, boardId=boardId, cts=datetime.now(), uts=datetime.now()))
    subBoard = await mongodb.engine.find(SubBoard, SubBoard.boardId == boardId)
    context["subBoards"] = subBoard
    context["boardId"] = boardId
    return templates.TemplateResponse("sub_board.html", context)


@router.post("/update", response_class=HTMLResponse)
async def subBoardUpdate(request: Request, subtitle: str = Form(...), desc: str = Form(...), boardId: ObjectId = Form(...), subBoardId: ObjectId = Form(...)):

    subBoard = await mongodb.engine.find_one(SubBoard, SubBoard.id == subBoardId)
    subBoard.title = subtitle
    subBoard.desc = desc
    subBoard.uts = datetime.now()
    await mongodb.engine.save(subBoard)

    board = await mongodb.engine.find_one(Board, Board.id == boardId)
    context = await validLogonCtx({"request": request, "title": title, "subname": subBoard.title + " 게시물 댓글"}, request)

    comments = await mongodb.engine.find(Comment, query.and_(Comment.subBoardId == subBoardId, Comment.boardId == boardId))
    context["comments"] = comments
    context["board"] = board
    context["subBoard"] = subBoard

    return templates.TemplateResponse("comment.html", context)


@router.post("/delete", response_class=HTMLResponse)
async def subBoardDelete(request: Request, boardId: ObjectId = Form(...), subBoardId: ObjectId = Form(...)):

    userid = request.cookies.get('userid')
    subBoard = await mongodb.engine.find_one(SubBoard, SubBoard.id == subBoardId)

    context = await validLogonCtx({"request": request, "title": title}, request)

    if (subBoard.userid == userid):
        await mongodb.engine.remove(SubBoard, SubBoard.id == subBoard.id)
        # defend comment remove
        await mongodb.engine.remove(Comment, Comment.subBoardId == subBoardId)
        context["boardmsg"] = subBoard.title+" 게시물이 삭제 되었습니다"
    else:
        context["boardmsg"] = "작성자만 삭제할 수 있습니다"
    sboard = await mongodb.engine.find(SubBoard, SubBoard.boardId == boardId)
    board = await mongodb.engine.find_one(Board, Board.id == boardId)

    if (sboard is not None):
        context["subBoards"] = sboard
        context["boardId"] = boardId
        context["board"] = board
    return templates.TemplateResponse("sub_board.html", context)
