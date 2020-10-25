import pytest

from server.shared.tracking_item_dal import *

def test_production_conn():
    prod_dal = TrackingItemDAL()
    one = prod_dal.run_sql("SELECT 1", {}, cursor_readscalar)
    assert one == 1

@pytest.fixture
def debugDal():
    debug_dal = TrackingItemDAL(True)
    
    #wipe test db out and add some static data
    tables = ["pricelog", "similaritem", "trackingitem", "trackinguser", "user_similar_items", "user_trackingitem"]
    for table in tables:
        debug_dal.run_sql("TRUNCATE TABLE " + table + " RESTART IDENTITY CASCADE", {})

    #load static data
    users = [
        {"user":"ems236@case.edu"}
    ]
    for user in users:
        debug_dal.run_sql("INSERT INTO trackinguser (userEmail, hasPrime) VALUES (%(user)s, true)", user)
        
    return debug_dal

def count(dal, tablename):
    return dal.run_sql("SELECT COUNT(*) FROM " + tablename, {}, cursor_readscalar)

def test_testconn(debugDal):
    one = debugDal.run_sql("SELECT 1", {}, cursor_readscalar)
    assert one == 1

def test_user_lookup(debugDal):
    assert count(debugDal, "trackinguser") == 1
    assert debugDal.userForEmail("ems236@case.edu") == 1
    assert count(debugDal, "trackinguser") == 1
    assert debugDal.userForEmail("ellis.saupe@gmail.com") == 2
    assert count(debugDal, "trackinguser") == 2