import sys
from typing import List
#import matplotlib.pyplot as plt

from classes import Schlumpf, Strategy, GameEngine, GameContext
from define_strategy import YourStrategy, YourSchlumpf



class Decider(Schlumpf):
    
    def get_response(self):
        self.been_drawn += 1
        
        if(self._inspect_is_lamp_active_()):
            self.count_schluempfe += 1 # Counter count_schluempfe is counting number of times they see an active lamp. 
            self._invert_lamp_()       # They are inverting the lamp when
        else:
            pass
        
        # Corresponds to Speaking
        if(self.count_schluempfe == self.current_game.get_member_number()-1):
            return self._ask_question_()
        else:
            return self._stay_quiet_()

class Lemming(Schlumpf):
    
    def get_response(self):
        self.been_drawn += 1
        if(self._inspect_is_lamp_active_()): #Lamp is active -> Do Nothing
            pass
        elif(self.toggled_lamps == 0): 
            self._invert_lamp_()
            self.toggled_lamps += 1
        
        return self._stay_quiet_()

class HopeForGod(Schlumpf):
    
    def get_response(self):
        self.been_drawn += 1
        schlmpfs = self.current_game.get_member_number()
        
        if(self.been_drawn > schlmpfs): #Wahrscheinlichkeit gezogen zu werden ist 1/N bei jedem Zug, d.h. Erwartungswert N Züge für Ein Mal gezogen, für N Mal gezogen: N^2
            return self._ask_question_()
        else:
            return self._stay_quiet_()        

class OptimalStrategy(Strategy):
    
    def generate_schluempfe(self) ->List:
        schls = [Lemming(i, self.engine) for i in range(self.member_number-1)]
        schls.append(Decider(self.member_number-1, self.engine))
        return schls

class ProbabilisticStrategy(Strategy):
    
    def generate_schluempfe(self) ->List:
        schls = [HopeForGod(i, self.engine) for i in range(self.member_number)]
        return schls


def main():
    amount = 0
    game = GameEngine(amount) #initializes Gargamel -> Gargamel captures amount schluempfe
                           
    strategys = [OptimalStrategy(GameContext()), ProbabilisticStrategy(GameContext())] #-> The schluempfe decide on their strategy (here, we have two separate runs with two strategys)
    
    for str in strategys:
        game.start(str)    #-> lets see what happens
    
    #results = []
    #for it in range(0, 10000):
    #    results.append(game.start(strategys[1]))
 
        
if __name__ == "__main__":
    main()