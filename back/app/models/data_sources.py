import datetime
from typing import List

from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship, backref

from back.app.schems import SystemItemType, SystemItemTag
from .db import Base
from ..schems.data_sources import DataSourcesStatus


class DataSources(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    status = Column(Enum(DataSourcesStatus), default=DataSourcesStatus.Connected, index=True)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now())
