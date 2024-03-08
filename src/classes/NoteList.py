import json
import logging

from classes.note import Note
from helpers import firebase

class NoteList():
    """
        This is a list of notes
    """
    def __init__(self, 
        CollectionID: str = "notes"):
        self.note_collection: list[Note] = []
        self.CollectionID = CollectionID

        #Build Note List
        self.BuildNoteList()

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

        RawResults = firebase.GetNoteList(CollectionId=self.CollectionID)

        print(f"Type: {type(RawResults)}, Count: {len(RawResults)}, Data: {RawResults}")
        # Itterate over results
        for aNote in RawResults:
            logging.debug(f"Type: {type(aNote)}")
            thisNote = Note.from_dict(data=aNote)
            self.note_collection.append(thisNote)