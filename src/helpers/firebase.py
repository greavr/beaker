import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from classes.note import Note

import logging
import cachetools.func
from datetime import datetime

def init_firebase():
    """ This function initalizes firebase for the app"""
    # Use the application default credentials.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

@cachetools.func.ttl_cache(maxsize=1024, ttl=5)
def GetNoteList(CollectionId: str = "notes") -> list:
    """ 
        This function returns all the notes in the collection
    
        Args:
            CollectionID: String - Name of the firestore collection to use, default is notes

        Returns:
            Dict List of JSON objects
    """
    #Return Value
    note_list = []

    try:
        # Attempting to list all notes available
        logging.info(f"Gather Notes from the {CollectionId}")
        db = firestore.client()
        docs = db.collection(CollectionId).get()
        
        for doc in docs:
            this_doc = doc.to_dict()
            print(this_doc["customer"])
            note_list.append(this_doc)
            this_doc = ""

        logging.debug(f"Found {len(note_list)} notes.")
    except Exception as ex:
        # Failed
        logging.error(ex)

    return note_list

def DeleteNote(NoteDetails: Note, CollectionId: str = "notes") -> bool:
    """ 
        This function removes note from collection 
    
        Args:
            NoteToDelete: Note - Note Object to remove
        
        Returns:
            Bool - True for success false for fail
    """
    record_id = NoteDetails.customer
    success = True

    try:
        db = firestore.client()
        notes_ref = db.collection(CollectionId)
        notes_ref.document(record_id).delete()

        success = True
    except Exception as ex:
        # Failed
        logging.error(ex)
        success = False

    return success

def Save(NoteDetails: Note, CollectionId: str = "notes") -> bool:
    """ 
        This function add and updates note in collection 
    
        Args:
            NoteDetails: Note - Note Object to add or update
        
        Returns:
            Bool - True for success false for fail
    """
    record_id = NoteDetails.customer
    NoteDetails.LastUpdated = datetime.now()
    success = True

    db = firestore.client()
    notes_ref = db.collection(CollectionId)
    notes_ref.document(record_id).set(NoteDetails.to_dict())
    
    success = True

    try:
        db = firestore.client()
        notes_ref = db.collection(CollectionId)
        notes_ref.document(record_id).set(NoteDetails.to_dict())
        
        success = True
    except Exception as ex:
        # Failed
        logging.error(ex)
        success = False

    return success