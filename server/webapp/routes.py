from flask import abort, request, jsonify, make_response, send_file 
from server.webapp import app

from server.shared import tracking_item_dal

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

@app.route('/hello')
def hello_world():
    return "Hello World"

@app.route('/item/register', methods=[POST])
def register_item():
    return abort(402)

@app.route('/item/update/sortorder', methods=[PUT])
def update_sort_order():
    return abort(402)

@app.route('/item/delete', methods=[DELETE])
def delete_item():
    return abort(402)

@app.route('/item/update/tracking', methods=[PUT])
def update_item():
    return abort(402)

@app.route('/notify/items', methods=[GET])
def notification_items():
    return abort(402)

@app.route('/similar/hide', methods=[POST])
def hide_similar():
    return abort(402)

@app.route('/similar/register', methods=[POST])
def register_similar():
    return abort(402)

@app.route('/user/isprime', methods=[GET])
def user_get_prime():
    return abort(402)

@app.route('/user/setprime', methods=[PUT])
def user_set_prime():
    return abort(402)