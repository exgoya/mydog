from odmantic import Model, EmbeddedModel, Field
from datetime import datetime
from typing import List, Union


class Comment(EmbeddedModel):
    desc: str
    cts: datetime = datetime.now()
    userid: str


class SubBoard(EmbeddedModel):
    title: str
    desc: str
    cts: datetime = datetime.now()
    uts: datetime = datetime.now()
    userid: str
    comment: Union[List[Comment], None] = None


class Board(Model):
    title: str = Field(unique=True)
    userid: str
    ts: datetime = datetime.now()
    subBoards: Union[List[SubBoard], None]
    # subBoards: {

    # }

    class Config:
        collection = "boards"


# from beanie import Document
# from datetime import datetime


# class Board(Document):
#     title: str
#     userid: str
#     ts: datetime = datetime.now()

#     class Settings:
#         name = "Board"

#     class Config:
#         schema_extra = {
#             "example": {
#                 "title": "슈나우저",
#                 "userid": "mydog",
#                 "date": datetime.now()
#             }
#         }

# class UpdateBoard()
