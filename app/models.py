from sqlalchemy import Column, Integer, String, Boolean, JSON, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from app.globals import SEOUL_TIMEZONE

Base = declarative_base()

class Statistic(Base):
  """방문자 통계"""
  __tablename__ = "statistic_tb"

  id = Column(Integer, primary_key=True, index=True)
  total_count = Column(Integer, nullable=False, default=0)
  last_updated_at = Column(DateTime, nullable=False)

class Session(Base):
  """세션"""
  __tablename__ = "session_tb"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(String(100), nullable=False, index=True)
  created_at = Column(DateTime, default=datetime.now(SEOUL_TIMEZONE), nullable=False)
  last_updated_at = Column(DateTime, default=datetime.now(SEOUL_TIMEZONE), nullable=False)


class ChatMessage(Base):
  """채팅 메시지"""
  __tablename__ = "chat_message_tb"

  id = Column(Integer, primary_key=True, index=True)
  session_id = Column(Integer, nullable=False, index=True, foreign_key=Session.id)
  sender_id = Column(String(100), nullable=False)
  receiver_id = Column(String(100), nullable=False)
  content = Column(String(1000), nullable=False)
  is_sent_to_telegram = Column(Boolean, default=False)
  created_at = Column(DateTime, default=datetime.now(SEOUL_TIMEZONE), nullable=False)

  def to_dict(self):
    return {
      "id": self.id,
      "session_id": self.session_id,
      "sender_id": self.sender_id,
      "receiver_id": self.receiver_id,
      "content": self.content,
      "is_sent_to_telegram": self.is_sent_to_telegram,
      "created_at": self.created_at
    }


# class Project(Base):
#   """프로젝트"""
#   __tablename__ = "project_tb"

#   id = Column(Integer, primary_key=True, index=True)
#   category = Column(String, nullable=True)
#   name = Column(String, nullable=False)
#   purpose = Column(String, nullable=False)
#   customer = Column(String, nullable=False)
#   start_date = Column(Date, nullable=False)
#   end_date = Column(Date, nullable=True)
#   is_done = Column(Boolean, nullable=False)
#   description = Column(JSON, nullable=False)
#   technologies = Column(JSON, nullable=False)
#   roles = Column(JSON, nullable=False)
#   results = Column(JSON, nullable=False)