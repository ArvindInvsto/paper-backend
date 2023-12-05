
import threading
import time
import os
from importlib.machinery import SourceFileLoader
strat_file_path = str(os.path.dirname(os.path.abspath(__file__))).replace('strategy_code','strategy_class_hl.py')
mod = SourceFileLoader("strat",strat_file_path).load_module()

class run_strategys(threading.Thread):
    def __init__(self, strat):
        threading.Thread.__init__(self)
        self.th_id = None
        self.counter = True
        self.strat = strat
        self.help_class = mod.BaseStrategyClass()

    def run(self):
        #strategy_ =  mod.Strategy.objects.using('strategydb').get(id=1)
        from datetime import datetime as dt
        self.th_id = threading.get_ident()
        while self.counter:
            print(threading.get_ident()) 
            now = dt.today().minute 
            if now %2 == 0: 
                print('buy ', now)
                self.help_class.buy(self.strat)
            else:
                print('sell', now)
                self.help_class.sell(self.strat)
            time.sleep(60)
    def kill(self):
        self.killed = True

