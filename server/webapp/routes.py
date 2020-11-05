from flask import abort, request, jsonify, make_response, send_file 
from server.webapp import app

from server.shared.tracking_item import TrackingItem
from server.shared.similar_item import SimilarItem
from server.shared.tracking_item_dal import TrackingItemDAL

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

def itemDAL():
    return TrackingItemDAL(app.config["IS_TEST"])

def makeSuccessResponse(dalFunc, *args):
    try: 
        response = {"success": dalFunc(itemDAL(), *args)}
        return jsonify(response)
    except Exception:
        abort(422)

def runQuery(dalFunc, *args):
    try: 
        return dalFunc(itemDAL(), *args)
    except Exception:
        return None

@app.route('/hello')
def hello_world():
    return "Hello World"

@app.route('/item/register', methods=[POST])
def register_item():
    item = TrackingItem.fromDict(request.json, TrackingItem.isValidInsert)
    if item is None:
        abort(422)
    
    return makeSuccessResponse(TrackingItemDAL.createItem, item, "ems236@case.edu")

@app.route('/item/update/tracking', methods=[PUT])
def update_item():
    item = TrackingItem.fromDict(request.json, TrackingItem.isValidUpdate)
    if item is None:
        abort(422)
    
    return makeSuccessResponse(TrackingItemDAL.updateItem, item, "ems236@case.edu")
        

@app.route('/item/update/sortorder', methods=[PUT])
def update_sort_order():
    if request.json is None or "itemIds" not in request.json:
        abort(422)
    itemIds = request.json["itemIds"]

    for id in itemIds:
        if not isinstance(id, int) or id <= 0:
            abort(422) 

    return makeSuccessResponse(TrackingItemDAL.updateSortOrder, "ems236@case.edu", itemIds)

@app.route('/item/delete', methods=[DELETE])
def delete_item():
    if request.json is None or "id" not in request.json:
        abort(422)
    id = request.json["id"]

    if not isinstance(id, int) or id <= 0:
        abort(422)
    
    return makeSuccessResponse(TrackingItemDAL.deleteItem, id, "ems236@case.edu")

@app.route('/notify/items', methods=[GET])
def notification_items():
    items = runQuery(TrackingItemDAL.notificationItems, "ems236@case.edu")
    
    if items is None:
        abort(422)
    
    itemList = []
    for item in items:
        itemDict = {
            "id": item.id,
            "priceThreshold": str(item.priceThreshold),
            "timeThreshold": item.timeThreshold.isoformat(),
            "url": item.url,
            "imgUrl": item.imgUrl,
            "title":item.title
        } 
        itemList.append(itemDict)

    return jsonify({"items": itemList})

@app.route('/similar/hide', methods=[POST])
def hide_similar():
    if request.json is None or "id" not in request.json:
        abort(422)
    id = request.json["id"]

    if not isinstance(id, int) or id <= 0:
        abort(422)
    
    return makeSuccessResponse(TrackingItemDAL.hideSimilar, id, "ems236@case.edu")

@app.route('/similar/register', methods=[POST])
def register_similar():
    item = SimilarItem.fromDict(request.json)
    if item is None:
        abort(422)
    
    return makeSuccessResponse(TrackingItemDAL.registerSimilar, item)

@app.route('/user/isprime', methods=[GET])
def user_get_prime():
    isPrime = runQuery(TrackingItemDAL.isUserPrime, "ems236@case.edu")
    
    if isPrime is None:
        abort(422)

    return jsonify({"isPrime": isPrime})

@app.route('/user/setprime', methods=[PUT])
def user_set_prime():
    if request.json is None or "isPrime" not in request.json:
        abort(422)
    isPrime = request.json["isPrime"]

    if not isinstance(isPrime, bool):
        abort(422)
    
    return makeSuccessResponse(TrackingItemDAL.updateUserPrime, "ems236@case.edu", isPrime)
    