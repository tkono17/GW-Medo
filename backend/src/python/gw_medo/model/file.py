from typing import Optional
from sqlmodel import SQLModel, Field, UniqueConstraint

#----------------------------------------------
# File
#----------------------------------------------
class FileBase(SQLModel):
    name: str = Field(index=True)
    path: str = Field(index=True)
    topic_id: Optional[int] = Field(default=None, foreign_key="topic.id")

class File(FileBase, table=True):
    __table_args__ = (UniqueConstraint('name', 'topic_id', name='unique_idx_name_topic_id'),)
    id: Optional[int] = Field(default=None, primary_key=True)

class FilePublic(FileBase):
    id: int

class FileCreate(FileBase):
    pass

class FileUpdate(FileBase):
    name: Optional[str] = None
    path: Optional[str] = None
    topic_id: Optional[int] = None
