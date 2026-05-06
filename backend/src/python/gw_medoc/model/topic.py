from typing import Optional
from dataclasses import dataclass, field
from sqlmodel import SQLModel, Field, Relationship
from .member import Member
from .event import Event

#----------------------------------------------
# Topic-X Links
#----------------------------------------------
class TopicMemberLink(SQLModel, table=True):
    topic_id: int = Field(foreign_key="topic.id", primary_key=True)
    member_id: int = Field(foreign_key="member.id", primary_key=True)

class TopicFileLink(SQLModel, table=True):
    topic_id: int = Field(foreign_key="topic.id", primary_key=True)
    file_id: int = Field(foreign_key="file.id", primary_key=True)

#----------------------------------------------
# Topic
#----------------------------------------------
class TopicBase(SQLModel):
    name: str = Field(index=True)
    duration: str|None = Field(default=None)
    startTime: str|None = Field(index=True, default=None)
    endTime: str|None = Field(index=True, default=None)
    event_id: int|None = Field(index=True, foreign_key='event.id', default=None)

class Topic(TopicBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    #event: Optional[Event] = Relationship(back_populates="topics")

    #members: list[Member] = Relationship(link_model=TopicMemberLink)
    #files: list["File"] = Relationship(link_model=TopicMemberLink)

#class TopicRead(TopicBase):
#    id: int

class TopicPublic(TopicBase):
    id: int

    #members: list[Member] = field(default_factory=list)
    #iles: list["File"] = field(default_factory=list)

class TopicCreate(TopicBase):
    members: list[Member] = field(default_factory=list)

class TopicUpdate(TopicBase):
    name: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    members: list[Member] | None = None
