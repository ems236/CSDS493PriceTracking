from .similar_item import SimilarItem
from .logged_price import LoggedPrice
from .tracking_item import TrackingItem

TEST_CONN_STR = ""
CONN_STR = ""

print(LoggedPrice(1, 1, 1))

class TrackingItemDAL:
    def __init__(self, isTest=False):
        self.connectionString = CONN_STR if not isTest else TEST_CONN_STR
    
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

     