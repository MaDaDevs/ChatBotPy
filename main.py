#!flask/bin/python
import os
import json
import string
import hashlib
import time
from flask import Flask, jsonify, abort, make_response, request, url_for, render_template, json, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from random import *


app = Flask(__name__, template_folder=".")
auth = HTTPBasicAuth()
authToken = HTTPTokenAuth(scheme='Token')


def get_token():
    min_char = 8
    max_char = 12
    allchar = string.ascii_letters + string.punctuation + string.digits
    token = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
    tokenJson = {"token": token}
    return tokenJson


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

token_manager = [
    {
        "str_token": "4231cb9ab06c4d4c3a8c7a3790bb3f98"
    }
]

message = {
    "text": "hi !"
}

erreurType = {
    "error": "not a valid type"
}

bye = {
    "text" : "See ya soon !"
}


@app.route('/login', methods = ['POST'])
def get_login():
    token = hashlib.md5()
    token.update(str(time.time()))
    t = token.hexdigest()
    object = {}
    object["str_token"] = t
    token_manager.append(object)
    return json.dumps(object)


@authToken.verify_token
def verify_token(token):
    for t in token_manager:
        if "str_token" in t and t["str_token"] == token:
            return True
    return False


@app.route('/actions', methods=['POST'])
@authToken.login_required
def actions():
    tab = []
    with open("bouton.json", "r") as file:
        user_data = json.load(file)
    if request.json["type"] == "message":
        if request.json["text"] == "hello":
            data = user_data["boutons"]["bouton_menu"]
            return json.dumps(data)
        else:
            return json.dumps(message)

    elif request.json["type"] == "button_tap" and request.json["payload"] :

        id = request.json["payload"]["button_id"]
        for j in user_data["boutons"]:
            if "parent_id" in user_data["boutons"][j] and user_data["boutons"][j]["parent_id"] == id:
                tab.append(user_data["boutons"][j])
        if not tab:
            return json.dumps(bye)
        return json.dumps(tab)

    else:

        return json.dumps(erreurType)


# def make_public_task(task):
#     new_task = {}
#     for field in task:
#         if field == 'id':
#             new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
#         else:
#             new_task[field] = task[field]
#     return new_task
#
#
# @app.route('/<string:page_name>', methods = ['GET'])
# def index(page_name):
#     if os.path.isfile(page_name):
#         return render_template("%s" % page_name)
#     else:
#         return render_template("error.html")
#
#
# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# @auth.login_required
# def get_tasks():
#     return jsonify({'tasks': map(make_public_task, tasks)})
#
#
# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
# @auth.login_required
# def get_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     return jsonify( { 'task': make_public_task(task[0]) } )
#
#
# @app.route('/todo/api/v1.0/tasks', methods = ['POST'])
# @auth.login_required
# def create_task():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify( { 'task': make_public_task(task) } ), 201
#
#
# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
# @auth.login_required
# def update_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if 'title' in request.json and type(request.json['title']) != unicode:
#         abort(400)
#     if 'description' in request.json and type(request.json['description']) is not unicode:
#         abort(400)
#     if 'done' in request.json and type(request.json['done']) is not bool:
#         abort(400)
#     task[0]['title'] = request.json.get('title', task[0]['title'])
#     task[0]['description'] = request.json.get('description', task[0]['description'])
#     task[0]['done'] = request.json.get('done', task[0]['done'])
#     return jsonify( { 'task': make_public_task(task[0]) } )
#
#
# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
# @auth.login_required
# def delete_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     tasks.remove(task[0])
#     return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)