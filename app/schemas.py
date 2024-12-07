# pydantic 스키마 정의
from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import date, datetime

# 통일된 응답 모델 정의
class ResponseModel(BaseModel):
    status: str
    data: Optional[Any]
    message: str

class WelcomeSchema(BaseModel):
  """페이지 진입시 기본 데이터 반환"""
  user_id: str
  isNewVisitor: bool

class StatisticSchema(BaseModel):
  """방문자 통계"""
  id: int
  total_count: int
  last_updated_at: datetime

  class Config:
    from_attributes = True


class SessionSchema(BaseModel):
  """세션"""
  id: int
  user_id: str
  created_at: datetime
  last_updated_at: datetime

  class Config:
    from_attributes = True

class SessionCreateSchema(BaseModel):
  """세션 생성"""
  user_id: str

  class Config:
    from_attributes = True


class ChatMessageSchema(BaseModel):
  """채팅 메시지"""
  id: int
  sender_id: str
  receiver_id: str
  content: str
  created_at: str
  is_sent_to_telegram: bool

  class Config:
    from_attributes = True


class ChatMessageCreateSchema(BaseModel):
  """채팅 메시지 생성"""
  sender_id: str
  receiver_id: str
  content: str

  class Config:
    from_attributes = True

class ChatMessageListRequestSchema(BaseModel):
  """채팅 메시지 목록 요청"""
  user_id: str

class ChatMessageListSchema(BaseModel):
    """채팅 메시지 목록"""
    user_id: str
    messages: Optional[List[ChatMessageSchema]]

    class Config:
        from_attributes = True


# class Project(BaseModel):
#   id: int
#   category: str
#   name: str
#   purpose: str
#   customer: str
#   start_date: date
#   end_date: Optional[date] = None;
#   is_done: bool
#   description: List[str]
#   technologies: List[str]
#   roles: List[str]
#   results: List[str]

#   class Config:
#     orm_mode = True

# class ProjectList(BaseModel):
#   """프로젝트 목록"""
#   projects: List[Project]

#   class Config:
#     orm_mode = True


# class ProjectDetail(BaseModel):
#   """프로젝트 상세"""
#   project: Project

#   class Config:
#     orm_mode = True


# class ProjectCreate(BaseModel):
#   """프로젝트 생성"""
#   category: str
#   name: str
#   purpose: str
#   customer: str
#   start_date: date
#   end_date: Optional[date] = None
#   is_done: bool
#   description: List[str]
#   technologies: List[str]
#   roles: List[str]
#   results: List[str]

#   class Config:
#     orm_mode = True