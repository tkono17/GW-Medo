from typing import Optional
from dataclasses import dataclass
from sqlmodel import SQLModel, Field, Relationship

from .category import Category

#----------------------------------------------
# EventType
#----------------------------------------------
class EventTypeBase(SQLModel):
    name: str = Field(index=True)

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
# Event-X Link
#----------------------------------------------
#lass EventTopicLink(SQLModel, table=True):
#   event_id: int = Field(foreign_key="event.id", primary_key=True)
#   topic_id: int = Field(foreign_key="topic.id", primary_key=True)

#----------------------------------------------
# Event
#----------------------------------------------
class EventBase(SQLModel):
    name: str = Field(index=True)
    startDatetime: str|None = Field(index=True, default=None)
    endDatetime: str|None = Field(index=True, default=None)
    place: str|None = Field(index=True, default=None)
    category_id: Optional[int] = Field(index=True, default=None, foreign_key="category.id")
    eventType_id: Optional[int] = Field(index=True, default=None, foreign_key="eventtype.id")

class Event(EventBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    #category: Category = Relationship(back_populates="events")
    #eventType: EventType = Relationship(back_populates="events")
    #topics: list["Topic"] = Relationship(back_populates="event")

class EventPublic(EventBase):
    id: int

    #category: Category | None = None
    #eventType: EventType | None = None
    #opics: list["Topic"] | None = None

#class EventPublic(EventBase):
#   id: int
#   eventType_id: int

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    name: Optional[str] = None
    startDatetime: Optional[str] = None
    endDatetime: Optional[str] = None
    place: Optional[str] = None
    category_id: Optional[int] = None
    eventType_id: Optional[int] = None
