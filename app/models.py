from sqlalchemy import Column, Integer, String, Boolean, JSON, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Statistic(Base):
  """방문자 통계"""
  __tablename__ = "statistic_tb"

  id = Column(Integer, primary_key=True, index=True)
  yesterday_count = Column(Integer, nullable=False, default=0)
  today_count = Column(Integer, nullable=False, default=0)
  total_count = Column(Integer, nullable=False, default=0)
  last_updated_at = Column(DateTime, nullable=False)



class Project(Base):
  """프로젝트"""
  __tablename__ = "project_tb"

  id = Column(Integer, primary_key=True, index=True)
  category = Column(String, nullable=True)
  name = Column(String, nullable=False)
  purpose = Column(String, nullable=False)
  customer = Column(String, nullable=False)
  start_date = Column(Date, nullable=False)
  end_date = Column(Date, nullable=True)
  is_done = Column(Boolean, nullable=False)
  description = Column(JSON, nullable=False)
  technologies = Column(JSON, nullable=False)
  roles = Column(JSON, nullable=False)
  results = Column(JSON, nullable=False)


class ChatMessage(Base):
  """채팅 메시지"""
  __tablename__ = "chat_message_tb"

  id = Column(Integer, primary_key=True, index=True)
  sender_id = Column(String, nullable=False)
  receiver_id = Column(String, nullable=False)
  content = Column(String, nullable=False)
  is_sent_to_telegram = Column(Boolean, default=False)
  created_at = Column(DateTime, nullable=False)

