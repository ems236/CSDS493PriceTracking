from .similar_item import SimilarItem
from .logged_price import LoggedPrice
from .tracking_item import TrackingItem

TEST_CONN_STR = ""
CONN_STR = ""

print(LoggedPrice(1, 1, 1))

class TrackingItemDAL:
    def __init__(self, isTest=False):
        self.connectionString = CONN_STR if not isTest else TEST_CONN_STR
    

     