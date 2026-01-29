from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class News(SQLModel, table=True):
    __tablename__ = "news"
    
    id: Optional[int] = Field(primary_key=True)
    title: str
    summary: str
    link: str
    img_link: str
    publiC_date: date
    regulatory_entity: str