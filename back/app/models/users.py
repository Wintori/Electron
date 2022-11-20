import datetime
from typing import List

from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship, backref

from back.app.schems import SystemItemType, SystemItemTag
from .db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    group_id = Column(Integer, ForeignKey("group.id"), index=True)
    group = relationship("Group", back_populates="users", foreign_keys=[group_id])
