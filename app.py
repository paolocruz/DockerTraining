from flask import Flask, redirect, url_for, \
				  request, render_template, json
from pymongo import MongoClient
import pymongo
import os
import socket
from bson import ObjectId



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


client = MongoClient('mongodb://backend:27017/dockerdemo')
db = client.blogpostDB

app = Flask(__name__)

@app.route("/")
def landing_page():
    posts = get_all_posts()
    
    return render_template('blog.html', posts=json.loads(posts))


@app.route('/add_post', methods=['POST'])
def add_post():

    new()
    return redirect(url_for('landing_page'))

@app.route('/update_post', methods=['POST'])
def update_post():

    update()
    return redirect(url_for('landing_page'))

@app.route('/delete-post/<post_id>', methods=['DELETE'])
def delete_post(post_id):

    delete_port_service(post_id)

    return {'message':"Successfully deleted."}, 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/remove_all')
def remove_all():
    db.blogpostDB.delete_many({})

    return redirect(url_for('landing_page'))




## Services

@app.route("/posts", methods=['GET'])
def get_all_posts():
    
    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]
    return JSONEncoder().encode(posts)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'title': request.form['title'],
        'post': request.form['post']
    }
    db.blogpostDB.insert_one(item_doc)

    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]

    return JSONEncoder().encode(posts[-1])

@app.route('/update', methods=['POST'])
def update():

    item = {'_id': ObjectId(request.form['id'])}
    item_doc = {
        'title': request.form['title'],
        'post': request.form['post']
    }
    db.blogpostDB.update(item, item_doc)

def delete_port_service(post_id):

    db.blogpostDB.remove({'_id':ObjectId(post_id)})

    _posts = db.blogpostDB.find({'_id':ObjectId(post_id)})
    return _posts

### Insert function here ###



############################



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
