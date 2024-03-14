import logging
import os
import random
import string
from datetime import datetime, timedelta, date

from helpers import cloudlogging, firebase


from classes import note, link, todo, NoteList

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_ckeditor import CKEditor


app = Flask(__name__)
ckeditor = CKEditor(app)
app.secret_key = "beakerbeaker"

@app.route("/note/<string:NoteTitle>", methods=['GET', 'POST'])
def read_note(NoteTitle):
    # Get IAP
    user = request.headers.get("X-Goog-Authenticated-User-Id")
    allNotes = NoteList.NoteList()
    allNotes.BuildNoteList()

    # Return Value
    found = False

    # Itterate through all notes
    for aNote in allNotes.note_collection:
        if aNote.customer == NoteTitle:
            foundNote = aNote.to_dict()
            found = True
    
    # Flash message
    if not found:
        flash(f'Unable to find note for: {NoteTitle}')

    return render_template('note.html', ThisNote=foundNote, User=user, NoteList=allNotes.note_collection, NoteTitles=allNotes.CustomerList,todoList=allNotes.todo_collection)

@app.route('/new')
def new_note():
    # Render new note age
    
    # Get IAP
    user = request.headers.get("X-Goog-Authenticated-User-Id")
    allNotes = NoteList.NoteList()
    allNotes.BuildNoteList()

    return render_template('note.html', ThisNote="", User=user, NoteList=allNotes.note_collection, NoteTitles=allNotes.CustomerList, todoList=allNotes.todo_collection)

@app.route("/delete/<string:DeleteNoteTitle>", methods=['GET', 'POST'])
def delete_note(DeleteNoteTitle):
    # This function deletes the note and rebuilds the notelist

    # Get IAP
    allNotes = NoteList.NoteList()
    allNotes.BuildNoteList()

    try:
        for aNote in allNotes.note_collection:
            if aNote.customer == DeleteNoteTitle:
                aNote.Delete()
                flash(f'Note for {DeleteNoteTitle} deleted successfully!', 'success')
                return redirect(url_for('index'))
        
        # Record not found
        flash(f'Note for {DeleteNoteTitle} not found!', 'error')
        print(url_for('read_note',NoteTitle=DeleteNoteTitle))
        return redirect(url_for('read_note',NoteTitle=DeleteNoteTitle))
    except Exception as ex:
        logging.error(ex)
        flash(f'Unable to delete: {DeleteNoteTitle}. Error: {ex}', 'error')
        return redirect(url_for('read_note',NoteTitle=DeleteNoteTitle))

@app.route('/settings')
def settings():
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get IAP
    user = request.headers.get("X-Goog-Authenticated-User-Id")
   
    # Render Home Page, Note list on left, and empty note in middle
    allNotes = NoteList.NoteList()
    allNotes.BuildNoteList()

    # Search found notes for the value in the customer or the notes attribute
    SearchPhrase = request.args.get('search')
    MatchingNotes = []
    if SearchPhrase:
        for aNote in allNotes.note_collection:
            if (aNote.customer.lower().find(SearchPhrase.lower()) != -1) or (aNote.Notes.lower().find(SearchPhrase.lower()) != -1):
                #Found a hit
                MatchingNotes.append(aNote)

    # Render Template
    return render_template('index.html', SearchTerm=SearchPhrase, SearchNotes=MatchingNotes, NoteList=allNotes.note_collection, User=user, todoList=allNotes.todo_collection)

@app.route('/save', methods=['POST'])
def save_note():
    this_note = note.Note(
        customer=request.form['customer'],
        fsr=request.form['fsr'],
        NextStep=request.form['NextStep'],
        Status=request.form['Status'],
        Images=[],
        Infrastructure=request.form['Infrastructure'],
        OnMe=request.form['OnMe'],
        SFDC=request.form['SFDC'],
        PublicSite=request.form['PublicSite'],
        Links=[],
        Todos=[],
        ExpertRequests=[],
        Notes=request.form.get('ckeditor')
    )

    # Validate safe
    if this_note.Save():
        flash(f'Note: {this_note.customer} saved successfully', 'success')
        return redirect("/", code=302)
    else:
        flash(f'Unable to delete: {this_note.customer}', 'error')
        return redirect(f"/note/{this_note.customer}?save=failed" , code=302)

if __name__ == '__main__':
    # First check if running in google cloud
    if os.getenv('is_gcp') is not None:
        cloudlogging.ConfigureCloudLogging()
    else:
        logging.info("Using local logs")

    # Now Configure Firebase
    firebase.init_firebase()

    # Testing time
    # Create Note
    thisCustomer = random.choice(["Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "George", "Hannah", "Ian", "Jack"])
    sampleNote = note.Note(
        customer=thisCustomer,
        fsr=random.choice(["Kaitlyn","Jimmy"]),
        Notes="BLAH BLAH BLAH",
        NextStep="Look into what we can do with Vertex",
        Status=random.choice(["Active","Closed"]),
        Images="",
        Infrastructure="Aws, with GKE and multiple Heroku instances",
        OnMe=True,
        SFDC=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)),
        PublicSite="https://www.netflix.com",
        Links=[link.link(url="https://www.google.com",text="Google"),link.link(url="https://reddit.com",text="Reddit")],
        ExpertRequests=[link.link(url="https://www.google.com",text="DocAI"),link.link(url="https://reddit.com",text="TTP")],
        Todos=[todo.todo(text="Look into vertex",status="Todo",DueDate=datetime.today() + timedelta(days=2), customer=thisCustomer),todo.todo(text="Sleep",status="Complete",customer=thisCustomer,DueDate=datetime.today() - timedelta(days=1)) ]
    )
    #sampleNote.Save()

    # Run the app
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))