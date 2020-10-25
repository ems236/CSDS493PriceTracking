import pytest

from server.shared.tracking_item_dal import *

def test_production_conn():
    prod_dal = TrackingItemDAL()
    one = prod_dal.run_sql("SELECT 1", {}, cursor_readscalar)
    assert one == 1

INITIAL_USERS = [
        {"user":"ems236@case.edu"}
        , {"user":"ellis.saupe@gmail.com"}
    ]

TEST_ITEM = TrackingItem.fromDBRecord(1, "testurl", "imgurl", "myitem", Decimal('1.25'), datetime.now(), 0, [])

TABLES = ["pricelog", "similaritem", "trackingitem", "trackinguser", "user_similar_item", "user_trackingitem"]
def wipeDB(debugDal):
    for table in TABLES:
        debugDal.run_sql("TRUNCATE TABLE " + table + " RESTART IDENTITY CASCADE", {})

@pytest.fixture
def debugDal():
    debug_dal = TrackingItemDAL(True)
    wipeDB(debug_dal)    
    return debug_dal

def count(dal, tablename):
    return dal.run_sql("SELECT COUNT(*) FROM " + tablename, {}, cursor_readscalar)

def test_testconn(debugDal):
    one = debugDal.run_sql("SELECT 1", {}, cursor_readscalar)
    assert one == 1

def test_nullable_scalar(debugDal):
    none = debugDal.run_sql("SELECT 1 WHERE 1 = 0", {}, cursor_readscalar_if_exists)
    assert none is None

    one = debugDal.run_sql("SELECT 1 WHERE 1 = 1", {}, cursor_readscalar_if_exists)
    assert 1 == 1

def test_user_lookup(debugDal):
    for user in INITIAL_USERS:
        debugDal.run_sql("INSERT INTO trackinguser (userEmail, hasPrime) VALUES (%(user)s, true)", user)

    assert count(debugDal, "trackinguser") == 2
    assert debugDal.userForEmail("ems236@case.edu") == 1
    assert count(debugDal, "trackinguser") == 2
    assert debugDal.userForEmail("ellis.saupe2@gmail.com") == 3
    assert count(debugDal, "trackinguser") == 3

    #TODO test equality

def test_item(debugDal):
    wipeDB(debugDal)

    assert count(debugDal, "trackingitem") == 0
    assert count(debugDal, "user_trackingitem") == 0
    debugDal.createItem(TEST_ITEM, INITIAL_USERS[0]["user"])
    assert count(debugDal, "trackingitem") == 1
    assert count(debugDal, "user_trackingitem") == 1

    #TODO test equality

def test_log_price(debugDal):
    wipeDB(debugDal)
    debugDal.createItem(TEST_ITEM, INITIAL_USERS[0]["user"])





