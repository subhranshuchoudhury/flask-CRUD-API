import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type"
    response.headers['Access-Control-Allow-Methods'] = "*"
    return response


class Note(db.Model):
    # unique key that defines the data.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    # 400 - size of the string, more than that will trimmed.
    content = db.Column(db.String(400), nullable=False)


with app.app_context():  # this is for creating uniques instances for users.
    db.create_all()  # for creating the db


@app.route("/")
def hello_world():
    return {"success": "true"}


@app.route("/test")
def test():
    return {"Hey": "Hello"}


@app.route("/notes/all", methods=["GET"])
def get_notes():
    notes = Note.query.all()
    noteList = []
    for i in notes:
        el = {}
        el["id"] = i.id
        el["title"] = i.title
        el["content"] = i.content
        noteList.append(el)
    return json.dumps(noteList)

# POST ROUTES


@app.route("/notes/add", methods=["POST"])
def post_note():
    note = Note(title=request.json["title"], content=request.json["content"])
    db.session.add(note)  # adding the data.
    # commit the data , it is the one step before the saving data.
    db.session.commit()
    noteList = {}
    noteList["id"] = note.id
    noteList["title"] = note.title
    noteList["content"] = note.content
    return json.dumps(noteList)

# PATCH ROUTES


@app.route("/notes/<int:id>", methods=["PATCH"])
def patch_note(id):  # get the id from the params.
    note = Note.query.get(id)
    note.title = request.json["title"]  # get the title from the request body.
    note.content = request.json["content"]
    db.session.commit()

    noteList = {}
    noteList["id"] = note.id
    noteList["content"] = note.content
    noteList["title"] = note.title

    return json.dumps(noteList)


@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):  # get the id from the params.
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()

    noteList = {}
    noteList["id"] = note.id
    noteList["content"] = note.content
    noteList["title"] = note.title

    return json.dumps(noteList)


if (__name__ == '__main__'):  # it checks that we are in the same file as the app.py
    app.run(debug=True)
