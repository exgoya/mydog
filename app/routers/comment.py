
from fastapi import APIRouter, Request, Form
from odmantic import query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.comment import Comment
from pathlib import Path
from app.routers.auth import Auth
from app.models import mongodb
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR/"templates")

router = APIRouter(
    prefix="/boards/cmt",
    tags=["commants"],
)
title = "mydog"

validLogonCtx = Auth.validLogonCtx


@router.get("/{boardTitle}/{subBoardTitle}", response_class=HTMLResponse)
async def getComment(request: Request, boardTitle: str, subBoardTitle: str, boardId: str, subBoardId: str):
    context = await validLogonCtx({"request": request, "title": title, "subname": subBoardTitle + " 게시물 댓글", "boardTitle": boardTitle, "subBoardTitle": subBoardTitle}, request)

    comments = await mongodb.engine.find(Comment, query.and_(Comment.subBoardId == subBoardId, Comment.boardId == boardId))

    if (comments is not None):
        context["comments"] = comments
        context["boardId"] = boardId
        context["subBoardId"] = subBoardId
    return templates.TemplateResponse("comment.html", context)


@router.post("/add", response_class=HTMLResponse)
async def commentAdd(request: Request, userid: str = Form(...), boardTitle: str = Form(...), subBoardTitle: str = Form(...), desc: str = Form(...), boardId: str = Form(...), subBoardId: str = Form(...)):

    context = await validLogonCtx({"request": request, "title": title, "subname": subBoardTitle + " 게시물 댓글", "boardTitle": boardTitle, "subBoardTitle": subBoardTitle}, request)

    await mongodb.engine.save(Comment(title=subBoardTitle, desc=desc, userid=userid, boardId=boardId, subBoardId=subBoardId))
    comments = await mongodb.engine.find(Comment, query.and_(Comment.subBoardId == subBoardId, Comment.boardId == boardId))
    context["comments"] = comments
    context["boardId"] = boardId
    context["subBoardId"] = subBoardId
    return templates.TemplateResponse("comment.html", context)
