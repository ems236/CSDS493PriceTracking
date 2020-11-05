import pytest
import json
from datetime import datetime
from decimal import Decimal
#pytest --cov-report term-missing --cov=server --pdb
from server.webapp import app
from server.shared.tracking_item_dal import TrackingItemDAL

@pytest.fixture
def api():
    app.config["IS_TEST"] = True
    yield app

@pytest.fixture
def client(api):
    #wipe test tables before trying anything
    debugDal = TrackingItemDAL(True)
    TABLES = ["pricelog", "similaritem", "trackingitem", "trackinguser", "user_similar_item", "user_trackingitem"]
    for table in TABLES:
        debugDal.run_sql("TRUNCATE TABLE " + table + " RESTART IDENTITY CASCADE", {})
    return api.test_client()

def test_hello(client):
    res = client.get("/hello")
    assert res.status_code == 200

def checkStatus(res, status):
    assert res.status_code == 200
    resData = json.loads(res.data)
    assert "success" in resData and resData["success"] == status

BAD_JSON = {"badAttr": 1
        , "token": 1
}
VALID_ITEM = {
        "url": "testurl",
        "imgUrl": "imgtest",
        "title": "amazonitem",
        "timeThreshold": datetime.now().isoformat(),
        "priceThreshold": "51.2",
        "sampleFrequency": 1
        , "token": 1
    }

def test_insertitem(client):
    res = client.post("/item/register", 
                    data=json.dumps(BAD_JSON),
                    content_type='application/json')
    assert res.status_code == 422

    res = client.post("/item/register", 
                    data=json.dumps(VALID_ITEM),
                    content_type='application/json')

    checkStatus(res, True)

def test_updateitem(client):
    client.post("/item/register", 
                    data=json.dumps(VALID_ITEM),
                    content_type='application/json')

    res = client.put("/item/update/tracking", 
                    data=json.dumps(BAD_JSON),
                    content_type='application/json')
    assert res.status_code == 422
    

    updateItem = {
        "id": 1,
        "timeThreshold": datetime.now().isoformat(),
        "priceThreshold": "51.1",
        "sampleFrequency": 2
        , "token": 1
    }

    res = client.put("/item/update/tracking", 
                    data=json.dumps(updateItem),
                    content_type='application/json')

    checkStatus(res, True)


def test_sortorder(client):
    client.post("/item/register", 
                    data=json.dumps(VALID_ITEM),
                    content_type='application/json')


    res = client.put("/item/update/sortorder", 
                    data=json.dumps(BAD_JSON),
                    content_type='application/json')
    assert res.status_code == 422

    badSort = {"itemIds": [-1, 1, 5]
        , "token": 1
    }
    res = client.put("/item/update/sortorder", 
                    data=json.dumps(badSort),
                    content_type='application/json')
    assert res.status_code == 422


    updateSort = {
        "itemIds": [1]
        , "token": 1
    }

    res = client.put("/item/update/sortorder", 
                    data=json.dumps(updateSort),
                    content_type='application/json')

    checkStatus(res, True)


def test_deleteitem(client):
    client.post("/item/register", 
                    data=json.dumps(VALID_ITEM),
                    content_type='application/json')

    res = client.delete("/item/delete", 
                    data=json.dumps(BAD_JSON),
                    content_type='application/json')
    assert res.status_code == 422

    badDelete = {"id": -1
        , "token": 1
    }
    res = client.delete("/item/delete", 
                    data=json.dumps(badDelete),
                    content_type='application/json')
    assert res.status_code == 422

    deleteItem = {
        "id": 1
        , "token": 1
    }

    res = client.delete("/item/delete", 
                    data=json.dumps(deleteItem),
                    content_type='application/json')

    checkStatus(res, True)


def test_notifyitem(client):
    res = client.get("/notify/items",
                    data=json.dumps({"token": 1}),
                    content_type='application/json')
    assert res.status_code == 200
    assert res.json is not None and "items" in res.json

    items = res.json["items"]
    assert len(items) == 0
    
    client.post("/item/register", 
                    data=json.dumps(VALID_ITEM),
                    content_type='application/json')
    
    testDal = TrackingItemDAL(True)
    testDal.logPrice(1, Decimal('1.5'), Decimal('1.5'))

    res = client.get("/notify/items",
                    data=json.dumps({"token": 1}),
                    content_type='application/json')
    assert res.status_code == 200
    assert res.json is not None and "items" in res.json

    items = res.json["items"]
    assert len(items) == 1


def test_getsetPrime(client):
    res = client.put("/user/setprime", 
                    data=json.dumps({"isPrime": 1
                    , "token":1
                    }),
                    content_type='application/json')
    assert res.status_code == 422

    res = client.put("/user/setprime", 
                    data=json.dumps({
                    "token":1
                    }),
                    content_type='application/json')
    assert res.status_code == 422

    res = client.put("/user/setprime", 
                    data=json.dumps({"isPrime": True
                    , "token":1
                    }),
                    content_type='application/json')
    checkStatus(res, True)
    
    res = client.get("/user/isprime", 
                    data=json.dumps({"token": 1}),
                    content_type='application/json')
    assert res.status_code == 200
    assert res.json is not None and "isPrime" in res.json
    isPrime = res.json["isPrime"]
    assert isPrime

    
VALID_SIMILAR_ITEM = {
    "itemUrl": "someUrl",
    "imgUrl": "somejpeg",
    "name": "mysimilar",
    "referrerItemId": 1,
    "price": "12.5",
    "token": 1
}

def test_registerSimilar(client):
    client.post("/item/register", 
                    data=json.dumps(VALID_ITEM),
                    content_type='application/json')

    res = client.post("/similar/register", 
                    data=json.dumps(BAD_JSON),
                    content_type='application/json')
    assert res.status_code == 422

    res = client.post("/similar/register", 
                    data=json.dumps(VALID_SIMILAR_ITEM),
                    content_type='application/json')

    checkStatus(res, True)

def test_hideSimilar(client):
    client.post("/item/register", 
                    data=json.dumps(VALID_ITEM),
                    content_type='application/json')
    client.post("/similar/register", 
                    data=json.dumps(VALID_SIMILAR_ITEM),
                    content_type='application/json')

    res = client.post("/similar/hide", 
                    data=json.dumps(BAD_JSON),
                    content_type='application/json')
    assert res.status_code == 422

    badDelete = {"id": -1
                    , "token":1
    }
    res = client.post("/similar/hide", 
                    data=json.dumps(badDelete),
                    content_type='application/json')
    assert res.status_code == 422

    deleteItem = {
        "id": 1
                    , "token":1
    }

    res = client.post("/similar/hide", 
                    data=json.dumps(deleteItem),
                    content_type='application/json')
    checkStatus(res, True)
