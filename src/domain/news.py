from datetime import date
from typing import Optional
from pydantic import HttpUrl, TypeAdapter

class New:
    
    def __init__(
        self,
        title: str,
        summary: str,
        link: str,
        img_link: str,
        public_date: date,
        regulatory_entity: str,
        id: Optional[int] = None):
        
        self.id = id
        self.title = title
        self.summary = summary
        self.link = link
        self.img_link = img_link
        self.date = public_date
        self.regulatory_entity = regulatory_entity
        
        self.validate()

    def validate(self):
        self._validate_links()
        self._validate_date()
        
    def _validate_links(self):
        url_adapter = TypeAdapter(HttpUrl)
        
        # Validamos el link de la noticia
        try:
            url_adapter.validate_python(self.link)
        except Exception:
            raise ValueError(f"El link de la noticia no es una URL válida: '{self.link}'. Asegúrate de que empiece con http:// o https://")

        # Validamos el link de la imagen
        try:
            url_adapter.validate_python(self.img_link)
        except Exception:
            raise ValueError(f"El link de la imagen no es una URL válida: '{self.img_link}'")
    
    def _validate_date(self):
        
        if self.date > date.today():
            raise ValueError("La fecha de publicación no puede ser una fecha futura")