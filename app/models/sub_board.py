from odmantic import Model, ObjectId
from datetime import datetime


class SubBoard(Model):
    title: str
    desc: str
    cts: datetime = datetime.now()
    uts: datetime = datetime.now()
    userid: str
    boardId: ObjectId

    class Config:
        collection = "sub_boards"
