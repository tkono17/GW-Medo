from typing import Optional
from dataclasses import dataclass
from sqlmodel import SQLModel, Field, UniqueConstraint

from .category import Category

#----------------------------------------------
# EventType
#----------------------------------------------
class EventTypeBase(SQLModel):
    name: str = Field(index=True, unique=True)

class EventType(EventTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    #event: "Event" = Relationship(back_populates="eventType")

class EventTypePublic(EventTypeBase):
    id: int

class EventTypeCreate(EventTypeBase):
    pass

class EventTypeUpdate(EventTypeBase):
    name: Optional[str] = None
    id: Optional[int] = None

#----------------------------------------------
# EventSession
#----------------------------------------------
class EventSessionBase(SQLModel):
    name: str = Field(index=True)
    date: str|None = Field(index=True, default=None)
    startTime: str|None = Field(index=True, default=None)
    endTime: str|None = Field(index=True, default=None)
    place: str|None = Field(index=True, default=None)
    category_id: Optional[int] = Field(index=True, default=None, foreign_key="category.id")
    eventType_id: Optional[int] = Field(index=True, default=None, foreign_key="eventtype.id")

class EventSession(EventSessionBase, table=True):
    __table_args__ = (UniqueConstraint('name', 'date', name='unique_idx_name_date'),)
    id: Optional[int] = Field(default=None, primary_key=True)

class EventSessionPublic(EventSessionBase):
    id: int

class EventSessionCreate(EventSessionBase):
    pass

class EventSessionUpdate(EventSessionBase):
    name: Optional[str] = None
    date: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    place: Optional[str] = None
    category_id: Optional[int] = None
    eventType_id: Optional[int] = None
