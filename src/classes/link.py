from datetime import datetime
import json

class link():
    def __init__(self, 
                 url: str, 
                 text: str, 
                 createdAt: datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                 ):
        self.url = url
        self.text = text
        self.createdAt = createdAt
    
    def __str__(self):
        return f"{self.url} - {self.text} - {self.createdAt}"
    
    def to_dict(self):
        return {
            "url": self.url,
            "text": self.text,
            "createdAt": self.createdAt
        }
    
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)

    def __repr__(self) -> str:
        return f"link('url={self.url}', text='{self.text}')"