from express import brokerage
import threading
from router.paperbrokerage.paperOrdersApi import paperOrdersApi


class AccessThreads:
    def __init__(self):
        self.dictionary = {}

    def add_thread(self, user_id, thread):
        self.dictionary[user_id] = thread
    
    def print_threads(self):
        print(self.dictionary)
    
    def kill_thread(self, user_id):
        if user_id in self.dictionary:
            thread = self.dictionary[user_id]
            thread.stop()
            del self.dictionary[user_id]
            return {"message":"successful"}
        else:
            return {"message":"User thread not found"}

my_dict = AccessThreads()
class run_brokerage(threading.Thread):
    def __init__(self, user_id):
        threading.Thread.__init__(self)
        self.bro_paper = brokerage.Paper()
        self.userid = user_id
        self.stop_event = threading.Event()
        self.ret = None
        
    def place_order(self, userid, trading_symbol, qty, exchange, trans_type, timestamp, product, order_type, price, stoploss_trigger, status):
        # self.ret = self.bro_paper.place_market_order(instrument="SBIN", exchange="NSE", order_side="BUY", qty=10, validity="DAY", variety="REGULAR", product_type="CNC")
        self.ret = paperOrdersApi.insert_paper_orders(userid=self.userid, trading_symbol=trading_symbol, qty=qty, exchange=exchange, trans_type=trans_type,
                                          timestamp=timestamp, product=product, order_type=order_type, price=price, stoploss_trigger=stoploss_trigger, status=status)

        return self.ret

    def stop(self):
        self.stop_event.set()    
