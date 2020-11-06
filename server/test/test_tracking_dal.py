import pytest
import psycopg2
#pytest --cov-config=.coveragerc --cov-report term-missing --cov=server/shared --pdb
from server.shared.tracking_item_dal import *

def test_production_conn():
    prod_dal = TrackingItemDAL()
    one = prod_dal.run_sql("SELECT 1", {}, cursor_readscalar)
    assert one == 1

#compare eq for that coverage
def test_bad_eq():
    x = TrackingItem.fromDBRecord(1, "testurl", "imgurl", "myitem", Decimal('1.25'), datetime.now(), TrackingItem.SAMPLE_DAY)
    y = SimilarItem(1, "a", 1, "none", "b", 0.0)
    z = LoggedPrice(datetime.now(), Decimal('1'), Decimal('2'))

    assert not x == y
    assert not y == x
    assert not z == x


def test_item_from_dict():
    VALID_ITEM = {
        "url": "testurl",
        "imgUrl": "imgtest",
        "title": "amazonitem",
        "timeThreshold": datetime.now().isoformat(),
        "priceThreshold": "51.2",
        "sampleFrequency": 1
    }

    testItem = TrackingItem.fromDict(None, TrackingItem.isValidInsert)
    assert testItem is None

    testItem = TrackingItem.fromDict(VALID_ITEM, TrackingItem.isValidInsert)
    assert testItem is not None

    VALID_ITEM["priceThreshold"] = "hello"
    testItem = TrackingItem.fromDict(VALID_ITEM, TrackingItem.isValidInsert)
    assert testItem is None

def test_similar_from_dict():
    VALID_SIMILAR_ITEM = {
        "itemUrl": "someUrl",
        "imgUrl": "somejpeg",
        "name": "mysimilar",
        "referrerItemId": 1,
        "price": "12.5"
    }

    testItem = SimilarItem.fromDict(None)
    assert testItem is None

    testItem = SimilarItem.fromDict(VALID_SIMILAR_ITEM)
    assert testItem is not None

    VALID_SIMILAR_ITEM["price"] = "-1.5"
    testItem = SimilarItem.fromDict(VALID_SIMILAR_ITEM)
    assert testItem is None

    VALID_SIMILAR_ITEM["price"] = "hello"
    testItem = SimilarItem.fromDict(VALID_SIMILAR_ITEM)
    assert testItem is None

def test_todict():
    x = TrackingItem.fromDBRecord(1, "testurl", "imgurl", "myitem", Decimal('1.25'), datetime.now(), TrackingItem.SAMPLE_DAY)
    y = SimilarItem(1, "a", 1, "none", "b", 0.0)
    z = LoggedPrice(datetime.now(), Decimal('1'), Decimal('2'))

    x.priceHistory.append(z)

    xDict = x.toDict()
    y.toDict()

    assert len(xDict["priceHistory"]) == 1

INITIAL_USERS = [
        {"user":"ems236@case.edu"}
        , {"user":"ellis.saupe@gmail.com"}
    ]

TEST_ITEM = TrackingItem.fromDBRecord(1, "testurl", "imgurl", "myitem", Decimal('1.25'), datetime.now(), TrackingItem.SAMPLE_DAY)
TEST_ITEM2 = TrackingItem.fromDBRecord(2, "testurl.com", "imgurl.png", "myitem2", Decimal('1.2'), datetime.now(), TrackingItem.SAMPLE_HOUR)
TEST_ITEM3 = TrackingItem.fromDBRecord(3, "testurl.biz", "imgurl.jpg", "myitem3", Decimal('1.29'), datetime.now(), TrackingItem.SAMPLE_WEEK)


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

#DAL-1,2
def test_user_lookup(debugDal):
    wipeDB(debugDal)
    for user in INITIAL_USERS:
        debugDal.run_sql("INSERT INTO trackinguser (userEmail, hasPrime) VALUES (%(user)s, true)", user)

    assert count(debugDal, "trackinguser") == 2
    #DAL-2
    assert debugDal.userForEmail("ems236@case.edu") == 1
    assert count(debugDal, "trackinguser") == 2
    #DAL-1
    assert debugDal.userForEmail("ellis.saupe2@gmail.com") == 3
    assert count(debugDal, "trackinguser") == 3

#DAL 15,16
def testPrimeGetSet(debugDal):
    wipeDB(debugDal)
    email = "ems236@case.edu"
    assert debugDal.userForEmail(email) == 1
    #DAL-16
    assert not debugDal.isUserPrime(email)
    #DAL-15
    assert debugDal.updateUserPrime(email, True)
    assert debugDal.isUserPrime(email)

#DAL-3,4,6,10,11,17,18
def test_single_item(debugDal):
    wipeDB(debugDal)

    test_email = INITIAL_USERS[0]["user"]

    assert count(debugDal, "trackingitem") == 0
    assert count(debugDal, "user_trackingitem") == 0
    #DAL-3
    debugDal.createItem(TEST_ITEM, test_email)
    assert count(debugDal, "trackingitem") == 1
    assert count(debugDal, "user_trackingitem") == 1

    #DAL-10
    items = debugDal.userItems(test_email)
    assert len(items) == 1
    assert items[0] == TEST_ITEM

    TEST_ITEM.priceThreshold += Decimal(100.06)
    #DAL-17
    assert debugDal.updateItem(TEST_ITEM, test_email)
    items = debugDal.userItems(test_email)
    assert len(items) == 1
    assert items[0] == TEST_ITEM

    #DAL-18
    TEST_ITEM.id = 100
    assert debugDal.updateItem(TEST_ITEM, test_email)
    items = debugDal.userItems(test_email)
    assert len(items) == 1
    TEST_ITEM.id = 1
    assert items[0] == TEST_ITEM

    #DAL-6
    assert debugDal.deleteItem(TEST_ITEM.id, test_email)
    #the item doesn't get deleted, just the fact that the user is tracking it
    assert count(debugDal, "trackingitem") == 1
    assert count(debugDal, "user_trackingitem") == 0

    #DAL-11
    items = debugDal.userItems(test_email)
    assert len(items) == 0

    #DAL-4
    debugDal.createItem(TEST_ITEM, test_email)
    assert count(debugDal, "trackingitem") == 1
    assert count(debugDal, "user_trackingitem") == 1

    TEST_ITEM.priceThreshold -= Decimal(100.06)


#DAL-5
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
    #DAL-5
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

#DAL-7,8,9
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

    #DAL-7
    for price in prices1:
        debugDal.logPrice(TEST_ITEM.id, price.price, price.primePrice)

    for price in prices2:
        debugDal.logPrice(TEST_ITEM2.id, price.price, price.primePrice)

    for price in prices3:
        debugDal.logPrice(TEST_ITEM3.id, price.price, price.primePrice)

    assert count(debugDal, "pricelog") == len(prices1) + len(prices2) + len(prices3)

    #DAL-9
    items = debugDal.userItems(test_email)
    assert len(items) == 3
    assert items[0] == TEST_ITEM
    assert items[1] == TEST_ITEM2
    assert items[2] == TEST_ITEM3

    #don't mess with test items persistently
    TEST_ITEM.priceHistory = []
    TEST_ITEM2.priceHistory = []
    TEST_ITEM3.priceHistory = []

    #DAL-8
    try:
        debugDal.logPrice(100, Decimal('15.7'), Decimal('13.0'))
        assert False
    except psycopg2.Error:
        assert True

#DAL 12,13,14
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

    #DAL-14
    items = debugDal.notificationItems(test_email)
    assert len(items) == 0

    price2 = LoggedPrice(datetime.min, Decimal('0.1'), Decimal('10.0'))
    debugDal.logPrice(TEST_ITEM.id, price2.price, price2.primePrice)

    #DAL-12
    items = debugDal.notificationItems(test_email)
    assert len(items) == 1
    assert items[0] == TEST_ITEM

    debugDal.logPrice(TEST_ITEM2.id, price.price, price.primePrice)
    debugDal.createItem(TEST_ITEM3, test_email)
    #DAL-13
    items = debugDal.notificationItems(test_email)
    
    assert len(items) == 2
    assert items[0] == TEST_ITEM
    assert items[1] == TEST_ITEM3


SIMILAR1 = SimilarItem(1, "testurl1", 1, "simboi", "ay.jpg", 0.0)
SIMILAR2 = SimilarItem(2, "testurl2", 1, "simboi2", "ayy.jpg", 0.0)
SIMILAR3 = SimilarItem(3, "testurl3", 1, "simboi3", "ayyy.jpg", 0.0)
SIMILAR4 = SimilarItem(4, "testurl4", 2, "simboi4", "ayyyy.jpg", 0.0)

#DAL-20,21,22,23,24,25
def test_similar_items(debugDal):
    wipeDB(debugDal)
    test_email = INITIAL_USERS[0]["user"]
    debugDal.createItem(TEST_ITEM, test_email)
    debugDal.createItem(TEST_ITEM2, test_email)

    assert count(debugDal, "similaritem") == 0
    #dal-23
    assert len(debugDal.similarItems(test_email, 1)) == 0

    #DAL-20
    debugDal.registerSimilar(SIMILAR1)
    debugDal.registerSimilar(SIMILAR2)
    debugDal.registerSimilar(SIMILAR3)
    debugDal.registerSimilar(SIMILAR4)


    #DAL-21
    try:
        debugDal.registerSimilar(SimilarItem(1, "testurl1", 1000, "simboi", "ay.jpg", 0.0))
        assert False
    except psycopg2.Error:
        assert True

    assert count(debugDal, "similaritem") == 4
    
    #DAL-22
    similars = debugDal.similarItems(test_email, 1)
    assert len(similars) == 3
    assert similars[0] == SIMILAR1
    assert similars[1] == SIMILAR2
    assert similars[2] == SIMILAR3

    #DAL-24
    assert debugDal.hideSimilar(3, test_email)
    similars = debugDal.similarItems(test_email, 1)
    assert len(similars) == 2
    assert similars[0] == SIMILAR1
    assert similars[1] == SIMILAR2


    #DAL-25
    try:
        debugDal.hideSimilar(1000, 1)
        assert False
    except psycopg2.Error:
        assert True

#DAL-19
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

    #DAL-19
    debugDal.updateSortOrder(test_email, [2, 3, 1])

    items = debugDal.userItems(test_email)
    assert len(items) == 3
    assert items[0] == TEST_ITEM2
    assert items[1] == TEST_ITEM3
    assert items[2] == TEST_ITEM

#DAL-26,27,28
def test_scrape_items(debugDal):
    wipeDB(debugDal)
    test_email1 = INITIAL_USERS[0]["user"]

    debugDal.createItem(TEST_ITEM, test_email1)
    debugDal.createItem(TEST_ITEM2, test_email1)
    debugDal.createItem(TEST_ITEM3, test_email1)

    #should be both of them
    #DAL-26
    items = debugDal.itemsToScrape(datetime(2020, 10, 25, 0, 0))
    assert len(items) == 3
    #DAL-27
    items = debugDal.itemsToScrape(datetime(2020, 10, 26, 0, 0))
    assert len(items) == 2
    #DAL-28
    items = debugDal.itemsToScrape(datetime(2020, 10, 25, 1, 0))
    assert len(items) == 1


def test_url_for_id(debugDal):
    wipeDB(debugDal)
    test_email1 = INITIAL_USERS[0]["user"]
    debugDal.createItem(TEST_ITEM, test_email1)

    url = debugDal.urlForItemId(1)
    assert url == TEST_ITEM.url

    url = debugDal.urlForItemId(100)
    assert url is None
