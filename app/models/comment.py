from odmantic import Model
from datetime import datetime


class Comment(Model):
    desc: str
    cts: datetime = datetime.now()
    userid: str
    subBoardId: str
    boardId: str

    class Config:
        collection = "comment"
