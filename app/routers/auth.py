
from fastapi import Request


class Auth:

    async def validLogonCtx(context: dict, request: Request):
        userid = request.cookies.get('userid')
        if (userid):
            context["logon"] = userid
            context["msg"] = "이미 로그인된 유저입니다."
        return context
