import pytest
import json
from datetime import datetime
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

def test_trackingitem(client):
    badItem = {"badAttr": 1}
    res = client.post("/item/register", 
                    data=json.dumps(badItem),
                    content_type='application/json')
    assert res.status_code == 422

    #"id", "url", "imgUrl", "title", "timeThreshold", "priceThreshold", "sampleFrequency"
    goodItem = {
        "url": "testurl",
        "imgUrl": "imgtest",
        "title": "amazonitem",
        "timeThreshold": datetime.now().isoformat(),
        "priceThreshold": "51.2",
        "sampleFrequency": 1
    }

    res = client.post("/item/register", 
                    data=json.dumps(goodItem),
                    content_type='application/json')

    checkStatus(res, True)

    res = client.put("/item/update/tracking", 
                    data=json.dumps(badItem),
                    content_type='application/json')
    assert res.status_code == 422
    

    updateItem = {
        "id": 1,
        "timeThreshold": datetime.now().isoformat(),
        "priceThreshold": "51.1",
        "sampleFrequency": 2
    }

    res = client.put("/item/update/tracking", 
                    data=json.dumps(updateItem),
                    content_type='application/json')

    checkStatus(res, True)


    res = client.put("/item/update/sortorder", 
                    data=json.dumps(badItem),
                    content_type='application/json')
    assert res.status_code == 422

    updateSort = {
        "itemIds": [1]
    }

    res = client.put("/item/update/sortorder", 
                    data=json.dumps(updateSort),
                    content_type='application/json')

    checkStatus(res, True)

    res = client.delete("/item/delete", 
                    data=json.dumps(badItem),
                    content_type='application/json')
    assert res.status_code == 422

    deleteItem = {
        "id": 1
    }

    res = client.delete("/item/delete", 
                    data=json.dumps(deleteItem),
                    content_type='application/json')

    checkStatus(res, True)

