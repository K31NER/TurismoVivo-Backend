from datetime import date
from typing import Optional
from pydantic import BaseModel, HttpUrl
from fastapi import Form

class NewsBase(BaseModel):
    title: str
    summary: str
    link: HttpUrl
    regulatory_entity: str

class NewsCreate(NewsBase):
    publiC_date: date = date.today()

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        summary: str = Form(...),
        link: str = Form(...),
        regulatory_entity: str = Form(...)
    ):
        return cls(
            title=title,
            summary=summary,
            link=link,
            regulatory_entity=regulatory_entity,
            publiC_date=date.today()
        )

class NewsUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    link: Optional[HttpUrl] = None
    regulatory_entity: Optional[str] = None
    publiC_date: Optional[date] = None

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Form(None),
        summary: Optional[str] = Form(None),
        link: Optional[str] = Form(None),
        regulatory_entity: Optional[str] = Form(None),
        publiC_date: Optional[date] = Form(None)
    ):
        data = {
            "title": title,
            "summary": summary,
            "link": link,
            "regulatory_entity": regulatory_entity,
            "publiC_date": publiC_date
        }
        return cls(**{k: v for k, v in data.items() if v is not None})

class NewsResponse(NewsBase):
    id: int
    img_link: HttpUrl
    publiC_date: date
