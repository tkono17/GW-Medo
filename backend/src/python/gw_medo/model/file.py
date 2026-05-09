from typing import Optional
from sqlmodel import SQLModel, Field

#----------------------------------------------
# File
#----------------------------------------------
class FileBase(SQLModel):
    name: str = Field(index=True)
    path: str = Field(index=True)
    topic_id: Optional[int] = Field(default=None, foreign_key="topic.id")

class File(FileBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class FilePublic(FileBase):
    id: int

class FileCreate(FileBase):
    pass

class FileUpdate(FileBase):
    name: Optional[str] = None
    path: Optional[str] = None
    topic_id: Optional[int] = None
