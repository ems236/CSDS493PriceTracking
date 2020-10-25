from decimal import * 

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
            (%(email)s, true)
        RETURNING id
        """

        return self.run_sql(USER_CREATE_SQL, USER_PARAMS, cursor_readscalar)


    def createItem(self, item: TrackingItem, userEmail: str):
        ITEM_SQL = """
        INSERT INTO trackingitem 
            (url, title, imgurl)
        VALUES
            (%(url)s, %(title)s, %(imgurl)s)
        RETURNING
            id
        """
        ITEM_PARAMS = {
            "url": item.url,
            "title": item.title,
            "imgurl": item.imgurl
            }
        
        itemid = self.run_sql(ITEM_SQL, ITEM_PARAMS, cursor_readscalar)
        userid = self.userForEmail(userEmail)

        USER_ITEM_SQL = """
        INSERT INTO user_trackingitem
            (itemId, userId, notifyDate, notifyPrice, sortOrder)
        VALUES
            (%(itemid)s, 
            %(userid)s, 
            %(notifyDate)s, 
            %(notifyPrice)s, 
            (SELECT 1 + MAX(sortOrder) FROM user_trackingitem WHERE userId = %(userid)s) 
            )
        """

        USER_ITEM_PARAMS = {
            "itemid": itemid,
            "userid":userid,
            "notifyDate":item.timeThreshold,
            "notifyPrice":item.priceThreshold,
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


    def updateItem(self, item: TrackingItem, userId: str):
        pass

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
        

    def notificationItems(self, userId: str):
        pass

    def similarItems(self, userId: str, itemId: int):
        pass

    def updateSortOrder(self, userId: str, itemIds: list, sortOrder: list):
        pass

    def registerSimilar(self, item: SimilarItem):
        pass

    def itemsToScrape(self):
        pass

     