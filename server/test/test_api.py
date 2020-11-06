import pytest
import json
from datetime import datetime
from decimal import Decimal
#pytest --cov-config=.coveragerc --cov-report term-missing --cov=server --pdb
from server.webapp import app
from server.shared.tracking_item_dal import TrackingItemDAL

from server.shared.tracking_item import TrackingItem
from server.shared.similar_item import SimilarItem

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

#IAPI-1,2
def test_insertitem(client):
    #IAPI-2
    res = client.post("/item/register", 
                    data=json.dumps(BAD_JSON),
                    content_type='application/json')
    assert res.status_code == 422

    #IAPI-1
    res = client.post("/item/register", 
                    data=json.dumps(VALID_ITEM),
                    content_type='application/json')

    checkStatus(res, True)

#IAPI-5,6
def test_updateitem(client):
    client.post("/item/register", 
                    data=json.dumps(VALID_ITEM),
                    content_type='application/json')

    #IAPI-6
    res = client.put("/item/update/tracking", 
                    data=json.dumps(BAD_JSON),
                    content_type='application/json')
    assert res.status_code == 422
    
    #IAPI-5
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

#IAPI-3
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

    #IAPI-3
    updateSort = {
        "itemIds": [1]
        , "token": 1
    }

    res = client.put("/item/update/sortorder", 
                    data=json.dumps(updateSort),
                    content_type='application/json')

    checkStatus(res, True)

#IAPI-4
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

    #IAPI-4
    deleteItem = {
        "id": 1
        , "token": 1
    }

    res = client.delete("/item/delete", 
                    data=json.dumps(deleteItem),
                    content_type='application/json')

    checkStatus(res, True)

#IAPI-11
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

#IAPI-12,13,14
def test_getsetPrime(client):
    #IAPI-14
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

    #IAPI-13
    res = client.put("/user/setprime", 
                    data=json.dumps({"isPrime": True
                    , "token":1
                    }),
                    content_type='application/json')
    checkStatus(res, True)
    
    #IAPI-12
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

#IAPI-7,8
def test_registerSimilar(client):
    #IAPI-8
    client.post("/item/register", 
                    data=json.dumps(VALID_ITEM),
                    content_type='application/json')

    res = client.post("/similar/register", 
                    data=json.dumps(BAD_JSON),
                    content_type='application/json')
    assert res.status_code == 422

    #IAPI-7
    res = client.post("/similar/register", 
                    data=json.dumps(VALID_SIMILAR_ITEM),
                    content_type='application/json')

    checkStatus(res, True)

#IAPI-9,10
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

    #IAPI-10
    badDelete = {"id": -1
                    , "token":1
    }
    res = client.post("/similar/hide", 
                    data=json.dumps(badDelete),
                    content_type='application/json')
    assert res.status_code == 422

    #IAPI-9
    deleteItem = {
        "id": 1
                    , "token":1
    }

    res = client.post("/similar/hide", 
                    data=json.dumps(deleteItem),
                    content_type='application/json')
    checkStatus(res, True)


TEST_ITEM = TrackingItem.fromDBRecord(1, "https://www.amazon.com/gp/product/B01D9OS5KA", "imgurl", "myitem", Decimal('1.25'), datetime.now(), TrackingItem.SAMPLE_DAY)
TEST_EMAIL = "ems236@case.edu"
TEST_SIMILAR_ITEM = SimilarItem(1, "testurl1", 1, "simboi", "ay.jpg", 0.0)
TOKEN_DICT = {"token": 1}
#IC-1, 2
def test_getItems(client):
    res = client.get("/dashboard/list", 
                    data=json.dumps(TOKEN_DICT),
                    content_type='application/json')
    
    assert res.status_code == 200
    assert res.json is not None and "items" in res.json and len(res.json["items"]) == 0

    #test noauth because we said we would
    #IC-2
    res = client.get("/dashboard/list", 
                    data=json.dumps({"nottoken": 1}),
                    content_type='application/json')
    
    assert res.status_code == 403


    debugDal = TrackingItemDAL(True)
    debugDal.createItem(TEST_ITEM, TEST_EMAIL)
    #IC-1
    #also test headers
    headers = {'Authorization': 'bearer 1'}
    res = client.get("/dashboard/list", 
                    data=json.dumps(TOKEN_DICT),
                    content_type='application/json',
                    headers=headers)
    
    assert res.status_code == 200
    assert res.json is not None and "items" in res.json and len(res.json["items"]) == 1
    assert "sampleFrequency" in res.json["items"][0]


#IC-3
def test_getSimilar(client):
    res = client.get("/dashboard/similaritems", 
                    data=json.dumps(TOKEN_DICT),
                    content_type='application/json')

    assert res.status_code == 422

    SIMILAR_REQ = {
        "token": 1,
        "itemId": 0
    }

    res = client.get("/dashboard/similaritems", 
                    data=json.dumps(SIMILAR_REQ),
                    content_type='application/json')

    assert res.status_code == 422


    SIMILAR_REQ = {
        "token": 1,
        "itemId": 1
    }
    res = client.get("/dashboard/similaritems", 
                    data=json.dumps(SIMILAR_REQ),
                    content_type='application/json')

    assert res.status_code == 200
    assert res.json is not None and "items" in res.json and len(res.json["items"]) == 0

    debugDal = TrackingItemDAL(True)
    debugDal.createItem(TEST_ITEM, TEST_EMAIL)
    debugDal.registerSimilar(TEST_SIMILAR_ITEM)

    res = client.get("/dashboard/similaritems", 
                    data=json.dumps(SIMILAR_REQ),
                    content_type='application/json')

    assert res.status_code == 200
    assert res.json is not None and "items" in res.json and len(res.json["items"]) > 1


