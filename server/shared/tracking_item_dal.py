from decimal import * 
from datetime import *

import psycopg2

from .similar_item import SimilarItem
from .logged_price import LoggedPrice
from .tracking_item import TrackingItem

TEST_CONN_STR = {
    'host': '127.0.0.1',
    'port': '5432',
    'user': 'webappuser',
    'password': 'webappuser',
    'dbname': 'test'
}

CONN_STR = {
    'host': '127.0.0.1',
    'port': '5432',
    'user': 'webappuser',
    'password': 'webappuser',
    'dbname': 'pricetracking'
}


def cursor_readscalar(cursor):
    return cursor.fetchone()[0]

def cursor_readscalar_if_exists(cursor):
    if cursor.rowcount == 0:
        return None
    else:
        return cursor.fetchone()[0]


def cursor_read_tracking_items_with_price(cursor):
    outVals = []
    current_id = -1
    current_item = None
    for row in cursor:
        #can't figure out string reading here
        if row[0] != current_id:
            current_item = TrackingItem.fromDBRecord(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            current_id = row[0]
            outVals.append(current_item)

        if row[7] is not None:
            current_item.priceHistory.append(LoggedPrice(row[7], row[8], row[9]))
    
    return outVals


def cursor_read_similar_items(cursor):
    outVals = []
    for row in cursor:
        current_item = SimilarItem(*row)
        outVals.append(current_item)
    
    return outVals

def cursor_read_tracking_items(cursor):
    outVals = []
    for row in cursor:
        current_item = TrackingItem.fromDBRecord(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        outVals.append(current_item)
    
    return outVals

def cursor_read_scrape_tuples(cursor):
    return cursor.fetchall()


class TrackingItemDAL:
    def __init__(self, isTest=False):
        self.connectionString = CONN_STR if not isTest else TEST_CONN_STR
    
    def run_sql(self, sql, params, cursor_func=None):
        with psycopg2.connect(**self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                if cursor_func is not None:
                    return cursor_func(cursor)
                else:
                    #means the query succeeded
                    return True

    def userForEmail(self, email:str):
        USER_EXISTS_SQL = """
        SELECT id 
        FROM trackinguser
        WHERE userEmail = %(email)s
        """

        USER_PARAMS = {"email": email}

        id = self.run_sql(USER_EXISTS_SQL, USER_PARAMS, cursor_readscalar_if_exists)

        if id is not None:
            return id

        #assume no prime, users change that later
        USER_CREATE_SQL = """
        INSERT INTO trackinguser
            (userEmail, hasPrime)
        VALUES
            (%(email)s, false)
        RETURNING id
        """

        return self.run_sql(USER_CREATE_SQL, USER_PARAMS, cursor_readscalar)


    def idForItem(self, item: TrackingItem):
        ITEM_EXISTS_SQL = """
        SELECT id
        FROM trackingitem
        WHERE url = %(url)s 
        """

        ITEM_PARAMS = {"url": item.url}
        id = self.run_sql(ITEM_EXISTS_SQL, ITEM_PARAMS, cursor_readscalar_if_exists)

        if id is not None:
            return id
        
        ITEM_CREATE_SQL = """
        INSERT INTO trackingitem 
            (url, title, imgurl)
        VALUES
            (%(url)s, %(title)s, %(imgurl)s)
        RETURNING
            id
        """
        ITEM_CREATE_PARAMS = {
            "url": item.url,
            "title": item.title,
            "imgurl": item.imgUrl
            }
        return self.run_sql(ITEM_CREATE_SQL, ITEM_CREATE_PARAMS, cursor_readscalar)


    def createItem(self, item: TrackingItem, userEmail: str):
        itemid = self.idForItem(item)
        userid = self.userForEmail(userEmail)

        USER_ITEM_SQL = """
        INSERT INTO user_trackingitem
            (itemId, userId, notifyDate, notifyPrice, sampleFrequency, sortOrder)
        VALUES
            (%(itemid)s, 
            %(userid)s, 
            %(notifyDate)s, 
            %(notifyPrice)s,
            %(sampleFrequency)s,
            (SELECT 1 + COALESCE(MAX(sortOrder), 0) FROM user_trackingitem WHERE userId = %(userid)s) 
            )
        ON CONFLICT DO NOTHING
        """

        USER_ITEM_PARAMS = {
            "itemid": itemid,
            "userid":userid,
            "notifyDate":item.timeThreshold,
            "notifyPrice":item.priceThreshold,
            "sampleFrequency":item.sampleFrequency
        }

        return self.run_sql(USER_ITEM_SQL, USER_ITEM_PARAMS)

        
    def deleteItem(self, itemId: int, userEmail: str):
        userId = self.userForEmail(userEmail)
        
        DELTE_ITEM_SQL = """
        DELETE FROM user_trackingitem ut
        WHERE ut.userId = %(userId)s AND ut.itemId = %(itemId)s
        """

        DELETE_PARAMS = {
            "userId": userId,
            "itemId": itemId
        }

        return self.run_sql(DELTE_ITEM_SQL, DELETE_PARAMS)


    def updateItem(self, item: TrackingItem, userEmail: str):
        userId = self.userForEmail(userEmail)

        UPDATE_ITEM_SQL = """
        UPDATE user_trackingitem 
        SET notifyDate = %(notifyDate)s,
            notifyPrice = %(notifyPrice)s,
            sampleFrequency = %(sampleFrequency)s
        WHERE itemId = %(itemId)s AND userId = %(userId)s
        """

        UPDATE_ITEM_PARAMS = {
            "notifyDate": item.timeThreshold,
            "notifyPrice": item.priceThreshold,
            "itemId": item.id,
            "userId": userId,
            "sampleFrequency": item.sampleFrequency
        }

        return self.run_sql(UPDATE_ITEM_SQL, UPDATE_ITEM_PARAMS)


    def logPrice(self, itemId: int, price: Decimal, primePrice: Decimal):
        LOG_SQL = """
        INSERT INTO pricelog
            (itemid, price, primePrice, logDate)
        VALUES
            (%(itemId)s, %(price)s, %(primePrice)s, now())
        """

        LOG_PARAMS = {
            "itemId": itemId,
            "price": price,
            "primePrice": primePrice 
        }

        return self.run_sql(LOG_SQL, LOG_PARAMS)
        

    def notificationItems(self, userEmail: str):
        userId = self.userForEmail(userEmail)

        ITEM_SQL = """
        SELECT i.id, i.url, i.imgurl, i.title, ui.notifyPrice, ui.notifyDate, ui.sampleFrequency
        FROM trackingitem i
        INNER JOIN user_trackingitem ui
        ON i.id = ui.itemId
        INNER JOIN trackinguser u
        ON ui.userId = u.id AND u.id = %(userId)s
        WHERE 
            ui.notifyDate <= now()
            OR ui.notifyPrice >=  
            (SELECT CASE WHEN u.hasPrime THEN l.primePrice ELSE l.price END
                FROM pricelog l
                WHERE
                    l.itemId = i.id
                    AND l.logDate = (SELECT MAX(ll.logDate) FROM pricelog ll WHERE ll.itemId = i.id)
            LIMIT 1)
        ORDER BY i.id
        """

        ITEM_PARAMS = {"userId": userId}
        return self.run_sql(ITEM_SQL, ITEM_PARAMS, cursor_read_tracking_items)


    def userItems(self, userEmail: str):
        userId = self.userForEmail(userEmail)

        ITEM_SQL = """
        SELECT i.id, i.url, i.imgurl, i.title, ui.notifyPrice, ui.notifyDate, ui.sampleFrequency, l.logDate, l.price, l.primePrice
        FROM trackingitem i
        INNER JOIN user_trackingitem ui
        ON i.id = ui.itemId
        INNER JOIN trackinguser u
        ON ui.userId = u.id 
        LEFT OUTER JOIN priceLog l
        ON i.id = l.itemId
        WHERE 
            u.id = %(userId)s
        ORDER BY ui.sortOrder, l.logDate
        """

        ITEM_PARAMS = {"userId": userId}
        return self.run_sql(ITEM_SQL, ITEM_PARAMS, cursor_read_tracking_items_with_price)


    def similarItems(self, userEmail: str, itemId: int):
        userId = self.userForEmail(userEmail)

        SIMILAR_SQL = """
        SELECT s.productUrl, s.itemId, s.productName, s.imageUrl, s.price
        FROM similaritem s
        WHERE s.itemId = %(itemId)s
            AND NOT EXISTS (SELECT 1 FROM user_similar_item us WHERE us.userId = %(userId)s AND us.similarid = s.id)
        """

        SIMILAR_PARAMS = {
            "userId": userId,
            "itemId": itemId
        }

        return self.run_sql(SIMILAR_SQL, SIMILAR_PARAMS, cursor_read_similar_items)


    def updateSortOrder(self, userEmail: str, itemIds: list):
        userId = self.userForEmail(userEmail)
        UPDATE_SQL = """
        UPDATE user_trackingitem
        SET sortOrder = %(sortOrder)s
        WHERE itemId = %(itemId)s AND userId = %(userId)s
        """

        update_params = {
            "sortOrder": 0,
            "itemId": 0,
            "userId": userId
        }

        isSuccess = True

        count = len(itemIds)
        counter = 1
        while isSuccess and counter <= count:
            update_params["itemId"] = itemIds[counter - 1]
            update_params["sortOrder"] = counter
            isSuccess = isSuccess and self.run_sql(UPDATE_SQL, update_params) 
            counter += 1

        return isSuccess


    def registerSimilar(self, item: SimilarItem):
        SIMILAR_SQL = """
        INSERT INTO similaritem
        (itemId, productName, productUrl, imageUrl, price)
        VALUES
        (%(itemId)s, %(productName)s, %(productUrl)s, %(imageUrl)s, %(price)s)
        """
        
        SIMILAR_PARAMS = {
            "itemId": item.referrerItemId,
            "productName": item.name,
            "productUrl": item.itemUrl,
            "imageUrl": item.imgUrl,
            "price": item.price
        }

        return self.run_sql(SIMILAR_SQL, SIMILAR_PARAMS)


    def hideSimilar(self, similaritemId: int, userEmail: int):
        userId = self.userForEmail(userEmail)
        
        HIDE_SQL = """
        INSERT INTO user_similar_item
        (similarId, userId)
        VALUES
        (%(itemId)s, %(userId)s)
        """

        HIDE_PARAMS = {
            "itemId": similaritemId, 
            "userId": userId
        }

        return self.run_sql(HIDE_SQL, HIDE_PARAMS)


    def updateUserPrime(self, userEmail: str, hasPrime: bool):
        userId = self.userForEmail(userEmail)

        PRIME_SQL = """
        UPDATE trackinguser 
        SET hasPrime = %(hasPrime)s
        WHERE id = %(userId)s
        """

        PRIME_PARAMS = {
            "userId": userId,
            "hasPrime": hasPrime
        }

        return self.run_sql(PRIME_SQL, PRIME_PARAMS)

    def isUserPrime(self, userEmail:str):
        userId = self.userForEmail(userEmail)

        PRIME_SQL = """
        SELECT hasPrime
        FROM trackinguser
        WHERE id = %(userId)s
        """

        PRIME_PARAMS = {
            "userId": userId,
        }

        return self.run_sql(PRIME_SQL, PRIME_PARAMS, cursor_readscalar)


    def itemsToScrape(self, date=datetime.now()):
        SCRAPE_SQL = """
        SELECT i.id, i.url
        FROM trackingitem i
        WHERE (SELECT MIN(ui.sampleFrequency) FROM user_trackingitem ui WHERE ui.itemId = i.id) 
            <= CASE 
            WHEN extract(dow from %(nowDate)s) = 0 AND extract(hour from %(nowDate)s) = 0 THEN 3 
            WHEN extract(hour from %(nowDate)s) = 0 THEN 2 
            ELSE 1 END
        ORDER BY i.id
        """

        SCRAPE_PARAMS = {
            "nowDate": date
        }

        return self.run_sql(SCRAPE_SQL, SCRAPE_PARAMS, cursor_read_scrape_tuples)

     