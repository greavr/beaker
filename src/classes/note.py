from datetime import datetime

import classes.todo as todo
import classes.link as link

import json

import helpers.firebase

class Note():
    """ THis is basic note class, used as home for all values"""
    def __init__(self, customer: str, fsr: str, NextStep: str, Status: str, Images: str, Infrastructure: str, OnMe: bool, SFDC: str, Todos: list[todo.todo], PublicSite: str, Links: list[link.link], Created: datetime = datetime.now()):
        self.customer = customer
        self.fsr = fsr
        self.NextStep = NextStep
        self.Status = Status
        self.Created =Created
        self.LastUpdated = datetime.now()
        self.Images = Images
        self.Infrastructure = Infrastructure
        self.OnMe = OnMe
        self.SFDC = SFDC
        self.Todos = Todos
        self.PublicSite = PublicSite
        self.Links = Links

    def __str__(self) -> str:
        return f"Note(customer={self.customer}, fsr={self.fsr}, NextStep={self.NextStep}, Status={self.Status}, Created={self.Created}, LastUpdated={self.LastUpdated}, Images={self.Images}, Infrastructure={self.Infrastructure}, OnMe={self.OnMe}, SFDC={self.SFDC}, Todos={self.Todos}, PublicSite={self.PublicSite}, Links={self.Links})"

    def __repr__(self):
        return f"Note('{self.customer}', '{self.fsr}', '{self.NextStep}', '{self.Status}', '{self.Created}', '{self.LastUpdated}', '{self.Images}', '{self.Infrastructure}', '{self.OnMe}', '{self.SFDC}', '{self.Todos}', '{self.PublicSite}', '{self.Links}')" 

    def to_dict(self):
        LinkList = []
        for aLink in self.Links:
            LinkList.append(aLink.to_dict())

        Todos = []
        for aTodo in self.Todos:
            Todos.append(aTodo.to_dict())

        return {
            "customer": self.customer,
            "fsr": self.fsr,
            "NextStep": self.NextStep,
            "Status": self.Status,
            "Created": self.Created,
            "LastUpdated": self.LastUpdated,
            "Images": self.Images,
            "Infrastructure": self.Infrastructure,
            "OnMe": self.OnMe,
            "SFDC": self.SFDC,
            "Todos": Todos,
            "PublicSite": self.PublicSite,
            "Links": LinkList
        }
    
    @classmethod
    def from_dict(self, data):
        Todos = []
        for aTodo in data["Todos"]:
            Todos.append(todo.todo.from_dict(data=aTodo))

        LinkList = []
        for aLink in data["Links"]:
            LinkList.append(link.link.from_dict(data=aLink))

        self.customer = data["customer"]
        self.fsr = data["fsr"]
        self.NextStep = data["NextStep"]
        self.Status = data["Status"]
        self.Created = data["Created"]
        self.LastUpdated = data["LastUpdated"]
        self.Images = data["Images"]
        self.Infrastructure = data["Infrastructure"]
        self.OnMe = data["OnMe"]
        self.SFDC = data["SFDC"]
        self.Todos = Todos
        self.PublicSite = data["PublicSite"]
        self.Links = LinkList

        return self

    @classmethod
    def from_json(self, data):
        self.from_dict(json.loads(data))
        return self

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)

    def Save(self, CollectionID: str = "notes") -> bool:
        """
            This saves the local file to firestore

            Args:
                CollectionID: String - The collection ID to save too
            Returns:
                Bool - Success upload or not
        """

        # Attempt upload to Firestore
        return helpers.firebase.Save(NoteDetails=self,CollectionId=CollectionID)
    
    def Delete(self, CollectionID: str = "notes") -> bool:
        """
            This deletes itself from firestore

            Args:
                CollectionID: String - The collection ID to save too
            Returns:
                Bool - Sucess of delete or not    
        """

        return helpers.firebase.DeleteNote(NoteDetails=self,CollectionId=CollectionID)
            