from sqlalchemy import Column, String, Integer

from .db import Base


class APIKeys(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    auth_string = Column(String, nullable=False)