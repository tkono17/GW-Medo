from typing import Optional
from dataclasses import dataclass, field
from sqlmodel import SQLModel, Field, UniqueConstraint
from .member import Member

#----------------------------------------------
# Topic-X Links
#----------------------------------------------
class TopicMemberLink(SQLModel, table=True):
    topic_id: int = Field(foreign_key="topic.id", primary_key=True)
    member_id: int = Field(foreign_key="member.id", primary_key=True)

#----------------------------------------------
# Topic
#----------------------------------------------
class TopicBase(SQLModel):
    name: str = Field(index=True)
    duration: str|None = Field(default=None)
    startTime: str|None = Field(index=True, default=None)
    endTime: str|None = Field(index=True, default=None)
    eventSession_id: int|None = Field(index=True, foreign_key='eventsession.id', default=None)

class Topic(TopicBase, table=True):
    __table_args = (
        UniqueConstraint('name', 'eventSession_id', name='unique_idx_name_eventSession_id'),
    )
    id: Optional[int] = Field(default=None, primary_key=True)

class TopicPublic(TopicBase):
    id: int

class TopicCreate(TopicBase):
    pass

class TopicUpdate(TopicBase):
    name: Optional[str] = None
    duration: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    eventSession_id: Optional[int] = None
