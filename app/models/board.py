from odmantic import Model, Field
from datetime import datetime


class Board(Model):
    title: str = Field(unique=True)
    userid: str
    ts: datetime = datetime.now()

    class Config:
        collection = "boards"
