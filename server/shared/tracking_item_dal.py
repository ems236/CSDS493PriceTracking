from functools import wraps

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

    def createItem(self, item: TrackingItem, userId: str):
        pass

    def deleteItem(self, itemId: int, userId: str):
        pass

    def updateItem(self, item: TrackingItem, userId: str):
        pass

    def logPrice(self, itemId: int, price: float, primePrice: float):
        pass

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

     