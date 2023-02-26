from odmantic import Model


class AuthModel(Model):
    userid: str
    password: str

    class Config:
        collection = "auths"
