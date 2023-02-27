
from beanie import Document
from datetime import datetime


class Board(Document):
    title: str
    ts: datetime
    userid: str
