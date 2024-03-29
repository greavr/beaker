from datetime import datetime

import classes.todo as todo
import classes.link as link

import json

import helpers.firebase

class Note():
    """ THis is basic note class, used as home for all values"""
    def __init__(self, 
                 customer: str, 
                 Notes:str, 
                 fsr: str, 
                 NextStep: str, 
                 Status: str, 
                 Images: str, 
                 Infrastructure: str, 
                 OnMe: bool, 
                 SFDC: str, 
                 PublicSite: str, 
                 Todos: list[todo.todo] = [], 
                 Links: list[link.link] = [],
                 ExpertRequests: list[link.link] = [], 
                 Created: datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
                 LastUpdated: datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
                 CollectionID: str = "notes"):
        self.customer = customer
        self.Notes = Notes
        self.fsr = fsr
        self.NextStep = NextStep
        self.Status = Status
        self.Created = Created
        self.LastUpdated = LastUpdated
        self.Images = Images
        self.Infrastructure = Infrastructure
        self.OnMe = OnMe
        self.SFDC = SFDC
        self.Todos = Todos
        self.PublicSite = PublicSite
        self.Links = Links
        self.ExpertRequests = ExpertRequests
        self.CollectionID = CollectionID

    def __str__(self) -> str:
        return f"Note(customer={self.customer}, Notes={self.Notes}, fsr={self.fsr}, NextStep={self.NextStep}, Status={self.Status}, Created={self.Created}, LastUpdated={self.LastUpdated}, Images={self.Images}, Infrastructure={self.Infrastructure}, OnMe={self.OnMe}, SFDC={self.SFDC}, Todos={self.Todos}, PublicSite={self.PublicSite}, Links={self.Links}, ExpertRequests={self.ExpertRequests})"

    def __repr__(self):
        return f"Note('{self.customer}', '{self.fsr}', '{self.NextStep}', '{self.Status}', '{self.Created}', '{self.LastUpdated}', '{self.Images}', '{self.Infrastructure}', '{self.OnMe}', '{self.SFDC}', '{self.Todos}', '{self.PublicSite}', '{self.Links}', '{self.ExpertRequests}')" 

    def to_dict(self):
        LinkList = []
        for aLink in self.Links:
            LinkList.append(aLink.to_dict())

        Todos = []
        for aTodo in self.Todos:
            Todos.append(aTodo.to_dict())

        ExpertList = []
        for aER in self.ExpertRequests:
                ExpertList.append(aER.to_dict())

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
            "Notes": self.Notes,
            "Links": LinkList,
            "ExpertRequests": ExpertList
        }

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
    
    def Delete(self) -> bool:
        """
            This deletes itself from firestore

            Args:
                CollectionID: String - The collection ID to save too
            Returns:
                Bool - Sucess of delete or not    
        """

        return helpers.firebase.DeleteNote(NoteDetails=self,CollectionId=self.CollectionID)
            