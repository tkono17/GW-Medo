from typing import Optional
from dataclasses import dataclass
from sqlmodel import SQLModel, Field

class MemberBase(SQLModel):
    name: str = Field(index=True, unique=True)
    position: str = Field(index=True)
    active: bool = Field(index=True)

class Member(MemberBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class MemberPublic(MemberBase):
    id: int

class MemberCreate(MemberBase):
    pass

class MemberUpdate(MemberBase):
    name: Optional[str] = None
    position: Optional[str] = None
    active: Optional[bool] = None
