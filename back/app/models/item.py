import datetime
from typing import List

from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship, backref

from back.app.schems import SystemItemType, SystemItemTag
from .db import Base


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String, nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    tag = Column(Enum(SystemItemTag), index=True, nullable=True)
    parent_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=True)
    type = Column(Enum(SystemItemType), nullable=False)
    size = Column(Integer, nullable=True, default=0)
    children: List["Items"] = relationship("Items", backref=backref("parent", remote_side=[id]),
                                           cascade="all, delete-orphan")

    def __str__(self):
        return f"Item {self.id = }  {self.url = }  {self.type = } {self.size = }  {self.date = }  "
