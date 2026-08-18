from sqlalchemy import Column, BigInteger
from src.db import Base


class Message(Base):
    __tablename__ = "message"

    message_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
