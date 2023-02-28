from odmantic import Model
from datetime import datetime


class Board(Model):
    title: str
    userid: str
    ts: datetime = datetime.now()

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
