from datetime import datetime
import json

class todo():
    def __init__(self, text: str, status: str, DueDate: datetime):
        self.text = text
        self.status = status
        self.DueDate = DueDate
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()

    def __str__(self) -> str:
        return f"todo: {self.text}, status: {self.status}, DueDate: {self.DueDate}, createdAt: {self.createdAt}, updatedAt: {self.updatedAt}"

    def to_dict(self):
        return {
            "text": self.text,
            "status": self.status,
            "DueDate": self.DueDate,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
    
    def __repr__(self) -> str:
        return f"todo(text: {self.text}, status: {self.status}, DueDate: {self.DueDate}, createdAt: {self.createdAt}, updatedAt: {self.updatedAt})"
    
    @classmethod
    def from_dict(self, data):
        self.text = data["text"]
        self.status = data["status"]
        self.DueDate = data["DueDate"]
        self.createdAt = data["createdAt"]
        self.updatedAt = data["updatedAt"]

        return self

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)
    
    @classmethod
    def from_json(self, data):
        self.from_dict(json.loads(data))
        return self
