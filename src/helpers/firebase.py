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

@cachetools.func.ttl_cache(maxsize=128, ttl=1)
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
            note_list.append(this_doc)

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
    NoteDetails.LastUpdated = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
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

def GetNote(DocName: str, CollectionId: str = "notes") -> dict:
    """
        This function looks up a note from the collection
        
        Ages: 
            DocName; Str - Name of the note to pull
            CollectionId: str - Note collection to search, default to notes
        
        Returns:
            Values to Dict
        
    """
    
    #Return Value
    ReturnDict = {}

    try:
        # Attempting to list all notes available
        logging.info(f"Gather Note {DocName} from the {CollectionId}")
        db = firestore.client()
        doc_ref = db.collection(CollectionId).document(DocName)
        doc = doc_ref.get()
        logging.debug(f"Found {DocName} notes.")
        ReturnDict = doc.to_dict()

    except Exception as ex:
        # Failed
        logging.error(ex)

    return ReturnDict