import pytest

from server.shared.tracking_item_dal import *

def test_production_conn():
    prod_dal = TrackingItemDAL()
    one = prod_dal.run_sql("SELECT 1", {}, cursor_readscalar)
    assert one == 1

@pytest.fixture
def debugDal():
    debug_dal = TrackingItemDAL(True)

    #wipe test db out

    return debug_dal

def test_testconn(debugDal):
    one = debugDal.run_sql("SELECT 1", {}, cursor_readscalar)
    assert one == 1