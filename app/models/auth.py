from odmantic import Model


class AuthModel(Model):
    id: str
    password: str

    class Config:
        collection = "auth"
