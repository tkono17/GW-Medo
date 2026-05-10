from typing import Optional
from dataclasses import dataclass
from sqlmodel import SQLModel, Field


#----------------------------------------------
# Category
#----------------------------------------------
class CategoryBase(SQLModel):
    name: str = Field(index=True, unique=True)

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    #events: list["Event"] = Relationship(back_populates="category")

class CategoryRead(CategoryBase):
    id: int

class CategoryPublic(CategoryBase):
    id: int

CategoryCreate = CategoryBase

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    id: Optional[int] = None
