from flask import abort, request, jsonify, make_response, send_file 
from server.webapp import app

from server.shared.tracking_item import TrackingItem
from server.shared.similar_item import SimilarItem
from server.shared.tracking_item_dal import TrackingItemDAL

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

itemDAL = TrackingItemDAL()

def makeSuccessResponse(dalFunc, *args):
    try: 
        response = {"success": dalFunc(itemDAL, *args)}
        return jsonify(response)
    except Exception:
        return abort(402)

@app.route('/hello')
def hello_world():
    return "Hello World"

@app.route('/item/register', methods=[POST])
def register_item():
    item = TrackingItem.fromDict(request.json, TrackingItem.isValidInsert)
    if item is None:
        return abort(402)
    
    return makeSuccessResponse(TrackingItemDAL.createItem, item, "ems236@case.edu")

@app.route('/item/update/tracking', methods=[PUT])
def update_item():
    item = TrackingItem.fromDict(request.json, TrackingItem.isValidUpdate)
    if item is None:
        return abort(402)
    
    return makeSuccessResponse(TrackingItemDAL.updateItem, item, "ems236@case.edu")
        

@app.route('/item/update/sortorder', methods=[PUT])
def update_sort_order():
    if request.json is None or "itemIds" not in request.json:
        return abort(402)
    itemIds = request.json["itemIds"]

    for id in itemIds:
        if not isinstance(id, int) or id <= 0:
            return abort(402) 

    return makeSuccessResponse(TrackingItemDAL.updateSortOrder, "ems236@case.edu", itemIds)

@app.route('/item/delete', methods=[DELETE])
def delete_item():
    if request.json is None or "id" not in request.json:
        return abort(402)
    id = request.json["id"]

    if not isinstance(id, int) or id <= 0:
        return abort(402)
    
    return makeSuccessResponse(TrackingItemDAL.deleteItem, id, "ems236@case.edu")



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