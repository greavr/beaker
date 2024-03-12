import json
import logging

from classes.note import Note
from classes.link import link
from classes.todo import todo

from helpers import firebase

class NoteList():
    """
        This is a list of notes
    """
    def __init__(self, CollectionID: str = "notes"):
        self.CustomerList = []
        self.note_collection = []
        self.CollectionID = CollectionID

    def __str__(self) -> str:
        return f"NoteList(notes={self.notes}) "

    def __repr__(self):
        return f"NoteList('{self.notes}')"

    def to_dict(self):
        return {
            "notes": [note.to_dict() for note in self.notes]
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def BuildNoteList(self):
        """ 
            This functions automatically builds list of notes from firebase
        """

        # Clean up the list
        self.note_collection = []

        RawResults = firebase.GetNoteList(CollectionId=self.CollectionID)

        # Itterate over results
        for aResult in RawResults:
            # Build Link list
            LinkList = []
            for aLink in aResult["Links"]:
                thisLink = link(
                    url=aLink["url"],
                    text=aLink["text"]
                )
                LinkList.append(thisLink)

            # Build Todo list
            TodoList = []
            for aTodo in aResult["Todos"]:
                thisTodo = todo(
                    text=aTodo["text"],
                    status=aTodo["status"],
                    DueDate=aTodo["DueDate"],
                    createdAt=aTodo["createdAt"],
                    updatedAt=aTodo["updatedAt"]
                )
                TodoList.append(thisTodo)


            thisNote = Note(
                customer=aResult["customer"],
                fsr=aResult["fsr"],
                NextStep=aResult["NextStep"],
                Status=aResult["Status"],
                Created=aResult["Created"],
                LastUpdated=aResult["LastUpdated"],
                Images=aResult["Images"],
                Infrastructure=aResult["Infrastructure"],
                OnMe=aResult["OnMe"],
                SFDC=aResult["SFDC"],
                Todos=TodoList,
                PublicSite=aResult["PublicSite"],
                Notes=aResult["Notes"],
                Links=LinkList,
                CollectionID=self.CollectionID
            )

            self.CustomerList.append(thisNote.customer)
            self.note_collection.append(thisNote)