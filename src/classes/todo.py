from datetime import datetime
import json

class todo():
    def __init__(self, text: str, status: str, DueDate: datetime, customer: str, updatedAt: datetime = datetime.now(), createdAt: datetime = datetime.now()):
        self.text = text
        self.status = status
        self.DueDate = DueDate.strftime("%m/%d/%Y, %H:%M:%S")
        self.createdAt = createdAt.strftime("%m/%d/%Y, %H:%M:%S")
        self.updatedAt = updatedAt.strftime("%m/%d/%Y, %H:%M:%S")
        self.customer = customer

    def __str__(self) -> str:
        return f"todo: {self.text}, customer: {self.customer}, status: {self.status}, DueDate: {self.DueDate}, createdAt: {self.createdAt}, updatedAt: {self.updatedAt}"

    def to_dict(self):
        return {
            "text": self.text,
            "customer": self.customer,
            "status": self.status,
            "DueDate": self.DueDate,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
    
    def __repr__(self) -> str:
        return f"todo(text: {self.text}, customer: {self.customer}, status: {self.status}, DueDate: {self.DueDate}, createdAt: {self.createdAt}, updatedAt: {self.updatedAt})"


    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)

