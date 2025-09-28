from typing import List
from classes import Schlumpf, Strategy, GameContext



class YourSchlumpf(Schlumpf):
    
    #HAS to implement/override get_response()
    
    def get_response(self):
        #
        # has to call at least self._stay_quiet_()
        #
        self._stay_quiet_()

class YourStrategy(Strategy):
    
    #HAS to implement/override generate_schluempfe() corresponding to their amount
    
    def generate_schluempfe(self) ->List:
        schlmpfs = [YourSchlumpf(0, GameContext())]
        return schlmpfs
    