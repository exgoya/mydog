from odmantic import Model, Field


class AuthModel(Model):
    userid: str = Field(unique=True)
    password: str

    class Config:
        collection = "auths"
