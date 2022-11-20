import datetime
from typing import List

from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship, backref

from back.app.schems import SystemItemType, SystemItemTag
from .db import Base


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    users = relationship("Users", back_populates="group")
