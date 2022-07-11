import secrets
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson import ObjectId

app = Flask(__name__)
app.config.from_json('config/production.json')
app.config['SECRET_KEY'] = secrets.token_hex(16)

ID = app.config['ID']


def create_mongodb_connection():
    user = app.config['MONGODB']['USER']
    pwd = app.config['MONGODB']['PASSWORD']
    host = app.config['MONGODB']['HOST']
    port = app.config['MONGODB']['PORT']
    database = app.config['MONGODB']['DATABASE']

    client = pymongo.MongoClient('mongodb://' + user + ':' + pwd + '@' + host + ':' + str(port))
    db = client[database]
    return db


@app.route("/")
def index():
    db = create_mongodb_connection()
    highlights = db.highlights.aggregate([
        {"$sample": {"size": 100}},
        {"$sort": {"vote_count": -1}}
    ])

    return render_template('index.html', highlights=list(highlights))


@app.route("/vote", methods=["POST"])
def vote():
    highlight_id = request.form['highlight_id']

    db = create_mongodb_connection()
    db.highlights.update_one(
        {"_id": ObjectId(highlight_id)},
        {"$inc": {"vote_count": 1}},
    )

    return redirect(url_for('index'))


@app.route("/edit", methods=["POST"])
def edit():
    highlight_id = request.form['highlight_id']

    db = create_mongodb_connection()
    db.highlights.update_one(
        {"_id": ObjectId(highlight_id)},
        {"$set": {"text": request.form['text']}},
    )

    return redirect(url_for('index'))


@app.route("/delete", methods=["POST"])
def delete():
    highlight_id = request.form['highlight_id']

    db = create_mongodb_connection()
    db.highlights.delete_one({"_id": ObjectId(highlight_id)})

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=ID + 10000)
