from odmantic import Model, ObjectId
from datetime import datetime


class Comment(Model):
    desc: str
    cts: datetime = datetime.now()
    userid: str
    subBoardId: ObjectId
    boardId: ObjectId

    class Config:
        collection = "comments"
