from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.models import mongodb
from app.models.book import BookModel
from app.models.auth import AuthModel
from .routers import board, sub_board, comment
from app.book_scraper import NaverBookScraper

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI()

app.include_router(board.router)
app.include_router(sub_board.router)
app.include_router(comment.router)

app.mount("/static", StaticFiles(directory=BASE_DIR/"static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR/"templates")
title = "mydog"


async def validLogonCtx(context: dict, request: Request):
    userid = request.cookies.get('userid')
    if (userid):
        context["logon"] = userid
        context["msg"] = "이미 로그인된 유저입니다."
    return context


@app.post("/auth/manage/update", response_class=HTMLResponse)
async def manageUpdate(request: Request, response: Response, userid: str = Form(...), password: str = Form(...)):
    auth = await mongodb.engine.find_one(AuthModel, AuthModel.userid == userid)
    auth.password = password
    await mongodb.engine.save(auth)

    context = {"request": request, "title": title,
               "subname": "변경"}
    return templates.TemplateResponse("index.html", await validLogonCtx(context, request))


@app.post("/auth/manage/delete", response_class=HTMLResponse)
async def manageDelete(request: Request, response: Response, userid: str = Form(...)):

    await mongodb.engine.remove(AuthModel, AuthModel.userid == userid)
    print("delete user!")
    context = {"request": request,
               "title": title, "subname": "변경"}

    response = templates.TemplateResponse(
        "index.html", context)
    response.delete_cookie("userid")
    print("delete cookie!")
    return response


@app.get("/auth/manage", response_class=HTMLResponse)
async def manage(request: Request):

    context = {"request": request, "title": title,
               "subname": "변경"}
    return templates.TemplateResponse("manageAuth.html", await validLogonCtx(context, request))


@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request, response: Response):
    response = templates.TemplateResponse(
        "index.html", {"request": request, "title": title})
    print("delete cookie!")
    response.delete_cookie("userid")
    return response


@app.post("/login")
async def login(request: Request, response: Response, userid: str = Form(...), password: str = Form(...)):

    auth = await mongodb.engine.find_one(AuthModel, AuthModel.userid == userid)

    if (auth is not None):
        if (auth.userid == userid):
            if (auth.password == password):
                response = templates.TemplateResponse(
                    "index.html", {"request": request, "title": title, "logon": userid})
                response.set_cookie("userid", userid)
                print("logcookie!" + userid)
                return response
    return templates.TemplateResponse("login.html", {"request": request, "title": title, "subname": "로그인", "msg": "회원정보가 맞지 않습니다. 다시 입력해주세요"})


@app.get("/login", response_class=HTMLResponse)
async def getLogin(request: Request):

    context = {"request": request, "title": title, "subname": "로그인"}

    return templates.TemplateResponse("login.html", await validLogonCtx(context, request))
    # book = BookModel(keyword="파이썬", publisher='BJPublic',
    #                  price=1200, image='me.png')
    # print(await mongodb.engine.save(book))


@app.get("/regist", response_class=HTMLResponse)
async def getRegist(request: Request):

    return templates.TemplateResponse("regist.html", {"request": request, "title": title, "subname": "회원가입"})


@app.post("/regist", response_class=HTMLResponse)
async def postRegist(request: Request, userid: str = Form(...), password: str = Form(...)):

    auth = AuthModel(userid=userid, password=password)
    print(auth)
    await mongodb.engine.save(auth)
    return templates.TemplateResponse("login.html", {"request": request, "title": title, "subname": "로그인", "msg": "회원가입 완료! 로그인 해주세요"})


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request, "title": title}
    return templates.TemplateResponse("index.html", await validLogonCtx(context, request))


@app.get("/validId", response_class=HTMLResponse)
async def validId(request: Request, userid: str):
    subname = "회원가입"
    context = {"request": request, "title": title, "subname": subname,
               "userid": userid, "validinfo": "사용가능한 아이디입니다"}
    if await mongodb.engine.find_one(AuthModel, AuthModel.userid == userid):
        print("exist userid")
        # userid = await mongodb.engine.find(AuthModel, AuthModel.userid == userid)
        context = {"request": request, "title": title, "subname": subname,
                   "userid": userid, "validinfo": "이미사용중인 아이디입니다"}
    return templates.TemplateResponse("regist.html", context)


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):

    # 1. 쿼리에서 검색어 추출
    keyword = q
    # (예외처리)
    #  - 검색어가 없다면 사용자에게 검색을 요구 return
    if not keyword:
        context = {"request": request, "title": title}
        print("debug -- no keyword")
        return templates.TemplateResponse(
            "./index.html",
            context
        )
    #  - 해당 검색어에 대해 수집된 데이터가 이미 DB에 존재한다면 해당 데이터를 사용자에게 보여준다. return
    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        print("exist keyword data")
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        return templates.TemplateResponse("./index.html", {"request": request, "title": title, "books": books},)

    # 2. 데이터 수집기로 해당 검색어에 대해 데이터를 수집한다.
    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(keyword, 10)
    book_models = []
    for book in books:
        book_model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            discount=book["discount"],
            image=book["image"],
        )
        book_models.append(book_model)
    # 3. DB에 수집된 데이터를 저장한다.
    await mongodb.engine.save_all(book_models)

    #  - 수집된 각각의 데이터에 대해서 DB에 들어갈 모델 인스턴스를 찍는다.
    #  - 각 모델 인스턴스를 DB에 저장한다.
    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": title, "books": books},
    )


@ app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("404.html", await validLogonCtx({"request": request, "title": title}, request))


@ app.on_event("startup")
def on_app_start():
    mongodb.connect()


@ app.on_event("shutdown")
async def on_app_shutdown():
    mongodb.close()
