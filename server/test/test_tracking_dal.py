import pytest
#pytest --cov=server/shared --pdb
from server.shared.tracking_item_dal import *

def test_production_conn():
    prod_dal = TrackingItemDAL()
    one = prod_dal.run_sql("SELECT 1", {}, cursor_readscalar)
    assert one == 1

INITIAL_USERS = [
        {"user":"ems236@case.edu"}
        , {"user":"ellis.saupe@gmail.com"}
    ]

TEST_ITEM = TrackingItem.fromDBRecord(1, "testurl", "imgurl", "myitem", Decimal('1.25'), datetime.now(), 0)
TEST_ITEM2 = TrackingItem.fromDBRecord(2, "testurl.com", "imgurl.png", "myitem2", Decimal('1.2'), datetime.now(), 0)
TEST_ITEM3 = TrackingItem.fromDBRecord(3, "testurl.biz", "imgurl.jpg", "myitem3", Decimal('1.29'), datetime.now(), 0)


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
    wipeDB(debugDal)
    for user in INITIAL_USERS:
        debugDal.run_sql("INSERT INTO trackinguser (userEmail, hasPrime) VALUES (%(user)s, true)", user)

    assert count(debugDal, "trackinguser") == 2
    assert debugDal.userForEmail("ems236@case.edu") == 1
    assert count(debugDal, "trackinguser") == 2
    assert debugDal.userForEmail("ellis.saupe2@gmail.com") == 3
    assert count(debugDal, "trackinguser") == 3

def testPrimeGetSet(debugDal):
    wipeDB(debugDal)
    email = "ems236@case.edu"
    assert debugDal.userForEmail(email) == 1
    assert not debugDal.isUserPrime(email)
    assert debugDal.updateUserPrime(email, True)
    assert debugDal.isUserPrime(email)


def test_single_item(debugDal):
    wipeDB(debugDal)

    test_email = INITIAL_USERS[0]["user"]

    assert count(debugDal, "trackingitem") == 0
    assert count(debugDal, "user_trackingitem") == 0
    debugDal.createItem(TEST_ITEM, test_email)
    assert count(debugDal, "trackingitem") == 1
    assert count(debugDal, "user_trackingitem") == 1

    items = debugDal.userItems(test_email)
    assert len(items) == 1
    assert items[0] == TEST_ITEM

    TEST_ITEM.priceThreshold += Decimal(100.06)
    assert debugDal.updateItem(TEST_ITEM, test_email)
    items = debugDal.userItems(test_email)
    assert len(items) == 1
    assert items[0] == TEST_ITEM

    assert debugDal.deleteItem(TEST_ITEM.id, test_email)
    #the item doesn't get deleted, just the fact that the user is tracking it
    assert count(debugDal, "trackingitem") == 1
    assert count(debugDal, "user_trackingitem") == 0
    items = debugDal.userItems(test_email)
    assert len(items) == 0

    TEST_ITEM.priceThreshold -= Decimal(100.06)



def test_many_item(debugDal):
    wipeDB(debugDal)

    test_email = INITIAL_USERS[0]["user"]

    assert count(debugDal, "trackingitem") == 0
    assert count(debugDal, "user_trackingitem") == 0
    debugDal.createItem(TEST_ITEM, test_email)
    assert debugDal.deleteItem(TEST_ITEM.id, test_email)
    #the item doesn't get deleted, just the fact that the user is tracking it
    assert count(debugDal, "trackingitem") == 1
    assert count(debugDal, "user_trackingitem") == 0
    
    #this duplicate is a sneaky way that broke the query earlier
    debugDal.createItem(TEST_ITEM, test_email)
    debugDal.createItem(TEST_ITEM, test_email)
    debugDal.createItem(TEST_ITEM2, test_email)
    debugDal.createItem(TEST_ITEM3, test_email)
    assert count(debugDal, "trackingitem") == 3
    assert count(debugDal, "user_trackingitem") == 3

    items = debugDal.userItems(test_email)
    assert len(items) == 3
    assert items[0] == TEST_ITEM
    assert items[1] == TEST_ITEM2
    assert items[2] == TEST_ITEM3


def test_log_price(debugDal):
    wipeDB(debugDal)
    test_email = INITIAL_USERS[0]["user"]

    debugDal.createItem(TEST_ITEM, test_email)
    debugDal.createItem(TEST_ITEM2, test_email)
    debugDal.createItem(TEST_ITEM3, test_email)

    prices1 = [LoggedPrice(datetime.now(), Decimal('12.7'), Decimal('10.0'))
                ,LoggedPrice(datetime.now(), Decimal('13.7'), Decimal('11.0'))
                , LoggedPrice(datetime.now(), Decimal('14.7'), Decimal('12.0'))
                ,LoggedPrice(datetime.now(), Decimal('15.7'), Decimal('13.0'))]
    prices2 = []
    prices3 = [LoggedPrice(datetime.now(), Decimal('1.0'), Decimal('10.0'))]

    TEST_ITEM.priceHistory = prices1
    TEST_ITEM2.priceHistory = prices2
    TEST_ITEM3.priceHistory = prices3

    for price in prices1:
        debugDal.logPrice(TEST_ITEM.id, price.price, price.primePrice)

    for price in prices2:
        debugDal.logPrice(TEST_ITEM2.id, price.price, price.primePrice)

    for price in prices3:
        debugDal.logPrice(TEST_ITEM3.id, price.price, price.primePrice)

    assert count(debugDal, "pricelog") == len(prices1) + len(prices2) + len(prices3)

    items = debugDal.userItems(test_email)
    assert len(items) == 3
    assert items[0] == TEST_ITEM
    assert items[1] == TEST_ITEM2
    assert items[2] == TEST_ITEM3

    #don't mess with test items persistently
    TEST_ITEM.priceHistory = []
    TEST_ITEM2.priceHistory = []
    TEST_ITEM3.priceHistory = []


def test_notification_items(debugDal):
    wipeDB(debugDal)

    test_email = INITIAL_USERS[0]["user"]
    TEST_ITEM.timeThreshold = datetime.max
    TEST_ITEM2.timeThreshold = datetime.max
    TEST_ITEM3.timeThreshold = datetime.min

    debugDal.createItem(TEST_ITEM, test_email)
    debugDal.createItem(TEST_ITEM2, test_email)

    price = LoggedPrice(datetime.min, Decimal('12.0'), Decimal('10.0'))
    debugDal.logPrice(TEST_ITEM.id, price.price, price.primePrice)

    items = debugDal.notificationItems(test_email)
    assert len(items) == 0

    price2 = LoggedPrice(datetime.min, Decimal('0.1'), Decimal('10.0'))
    debugDal.logPrice(TEST_ITEM.id, price2.price, price2.primePrice)

    items = debugDal.notificationItems(test_email)
    assert len(items) == 1
    assert items[0] == TEST_ITEM

    debugDal.logPrice(TEST_ITEM2.id, price.price, price.primePrice)
    debugDal.createItem(TEST_ITEM3, test_email)
    items = debugDal.notificationItems(test_email)
    
    assert len(items) == 2
    assert items[0] == TEST_ITEM
    assert items[1] == TEST_ITEM3


SIMILAR1 = SimilarItem("testurl1", 1, "simboi", "ay.jpg")
SIMILAR2 = SimilarItem("testurl2", 1, "simboi2", "ayy.jpg")
SIMILAR3 = SimilarItem("testurl3", 1, "simboi3", "ayyy.jpg")
SIMILAR4 = SimilarItem("testurl4", 2, "simboi4", "ayyyy.jpg")

def test_similar_items(debugDal):
    wipeDB(debugDal)
    test_email = INITIAL_USERS[0]["user"]
    debugDal.createItem(TEST_ITEM, test_email)
    debugDal.createItem(TEST_ITEM2, test_email)

    assert count(debugDal, "similaritem") == 0
    assert len(debugDal.similarItems(test_email, 1)) == 0

    debugDal.registerSimilar(SIMILAR1)
    debugDal.registerSimilar(SIMILAR2)
    debugDal.registerSimilar(SIMILAR3)
    debugDal.registerSimilar(SIMILAR4)

    assert count(debugDal, "similaritem") == 4
    similars = debugDal.similarItems(test_email, 1)
    assert len(similars) == 3
    assert similars[0] == SIMILAR1
    assert similars[1] == SIMILAR2
    assert similars[2] == SIMILAR3

    assert debugDal.hideSimilar(3, test_email)
    similars = debugDal.similarItems(test_email, 1)
    assert len(similars) == 2
    assert similars[0] == SIMILAR1
    assert similars[1] == SIMILAR2

def test_sort_order(debugDal):
    wipeDB(debugDal)
    test_email = INITIAL_USERS[0]["user"]
    debugDal.createItem(TEST_ITEM, test_email)
    debugDal.createItem(TEST_ITEM2, test_email)
    debugDal.createItem(TEST_ITEM3, test_email)

    items = debugDal.userItems(test_email)
    assert len(items) == 3
    assert items[0] == TEST_ITEM
    assert items[1] == TEST_ITEM2
    assert items[2] == TEST_ITEM3

    debugDal.updateSortOrder(test_email, [1, 2, 3], [3, 1, 2])

    items = debugDal.userItems(test_email)
    assert len(items) == 3
    assert items[0] == TEST_ITEM2
    assert items[1] == TEST_ITEM3
    assert items[2] == TEST_ITEM


    
