from datetime import datetime
import json

class todo():
    def __init__(self, text: str, status: str, DueDate: datetime, updatedAt: datetime = datetime.now(), createdAt: datetime = datetime.now()):
        self.text = text
        self.status = status
        self.DueDate = DueDate
        self.createdAt = createdAt
        self.updatedAt = updatedAt

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


    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)

