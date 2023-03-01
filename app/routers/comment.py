
from fastapi import APIRouter, Request, Form
from odmantic import ObjectId, query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.comment import Comment
from app.models.sub_board import SubBoard
from app.models.board import Board
from pathlib import Path
from app.routers.auth import Auth
from app.models import mongodb
from datetime import datetime
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR/"templates")

router = APIRouter(
    prefix="/boards/cmt",
    tags=["commants"],
)
title = "mydog"

validLogonCtx = Auth.validLogonCtx


@router.get("/{boardId}/{subBoardId}", response_class=HTMLResponse)
async def getComment(request: Request, boardId: ObjectId, subBoardId: ObjectId):

    comments = await mongodb.engine.find(Comment, query.and_(Comment.subBoardId == subBoardId, Comment.boardId == boardId))
    subBoard = await mongodb.engine.find_one(SubBoard, SubBoard.id == subBoardId)
    board = await mongodb.engine.find_one(Board, Board.id == boardId)

    context = await validLogonCtx({"request": request, "title": title, "subname": subBoard.title + " 게시물 댓글"}, request)

    if (comments is not None):
        context["comments"] = comments
        context["subBoard"] = subBoard
        context["board"] = board
    return templates.TemplateResponse("comment.html", context)


@router.post("/add", response_class=HTMLResponse)
async def commentAdd(request: Request, userid: str = Form(...), boardId: ObjectId = Form(...), subBoardId: ObjectId = Form(...), desc: str = Form(...)):

    subBoard = await mongodb.engine.find_one(SubBoard, SubBoard.id == subBoardId)
    board = await mongodb.engine.find_one(Board, Board.id == boardId)
    context = await validLogonCtx({"request": request, "title": title, "subname": subBoard.title + " 게시물 댓글"}, request)

    await mongodb.engine.save(Comment(desc=desc, userid=userid, boardId=boardId, subBoardId=subBoardId, cts=datetime.now()))
    comments = await mongodb.engine.find(Comment, query.and_(Comment.subBoardId == subBoardId, Comment.boardId == boardId))
    context["comments"] = comments
    context["board"] = board
    context["subBoard"] = subBoard

    return templates.TemplateResponse("comment.html", context)


@router.get("/delete", response_class=HTMLResponse)
async def removeCmt(request: Request, cmtId: ObjectId):
    print(cmtId)
    userid = request.cookies.get('userid')
    cmt = await mongodb.engine.find_one(Comment, Comment.id == cmtId)
    print("xxxxxxx")
    print(cmt)
    comments = await mongodb.engine.find(Comment, Comment.subBoardId == cmt.subBoardId)
    subBoard = await mongodb.engine.find_one(SubBoard, SubBoard.id == cmt.subBoardId)
    board = await mongodb.engine.find_one(Board, Board.id == cmt.boardId)

    context = await validLogonCtx({"request": request, "title": title, "subname": subBoard.title + " 게시물 댓글"}, request)
    if (userid == cmt.userid):
        await mongodb.engine.remove(Comment, Comment.id == cmt.id)
        context["boardmsg"] = "삭제 되었습니다"
    else:
        context["boardmsg"] = "작성자만 삭제할 수 있습니다"

    if (comments is not None):
        context["comments"] = comments
        context["subBoard"] = subBoard
        context["board"] = board
    return templates.TemplateResponse("comment.html", context)
