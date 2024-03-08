import logging
import os
import random
import string
from datetime import datetime, timedelta
from helpers import cloudlogging, firebase

from classes import note, link, todo, NoteList

from flask import Flask, render_template, request, redirect, url_for, send_from_directory


app = Flask(__name__)

@app.route('/')
def index():
    # Render Home Page, Note list on left, and empty note in middle
    allNotes = NoteList.NoteList()
    allNotes.BuildNoteList()

    # Build NodeTitle List
    NoteTitles = []
    for aNote in allNotes.note_collection:
        NoteTitles.append(aNote.customer)

    # Render Template
    return render_template('index.html', NoteList=NoteTitles)

@app.route('/save')
def save_note():
    this_note = note.Note(
        customer=request.form['customer'],
        fsr=request.form['fsr'],
        NextStep=request.form['NextStep'],
        Status=request.form['Status'],
        Images=request.form['Images'],
        Infrastructure=request.form['Infrastructure'],
        OnMe=request.form['OnMe'],
        SFDC=request.form['SFDC'],
        PublicSite=request.form['PublicSite'],
        Links=[],
        Todos=[],
    )

    # Validate safe
    if this_note.save():
        return redirect("/?save=success", code=302)
    else:
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
    aNote = note.Note(
        customer=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
        fsr=random.choice(["Kaitlyn","Jimmy"]),
        NextStep="Look into what we can do with Vertex",
        Status=random.choice(["Active","Closed"]),
        Images="",
        Infrastructure="Aws, with GKE and multiple Heroku instances",
        OnMe=True,
        SFDC="12345sadfg",
        PublicSite="https://www.netflix.com",
        Links=[link.link(url="https://www.google.com",text="Google"),link.link(url="https://reddit.com",text="Reddit")],
        Todos=[todo.todo(text="Look into vertex",status="Todo",DueDate=datetime.today() + timedelta(days=2)),todo.todo(text="Sleep",status="Complete",DueDate=datetime.today() - timedelta(days=1)) ]
    )
    #aNote.Save()

    # Run the site
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))