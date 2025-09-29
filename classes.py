#from typing import List
from abc import ABC, abstractmethod

from numpy import random            

class Strategy (ABC):
    """
    Abstract Strategy Class
    
    
    """
    
    def __init__(self, engine = None):
        self.engine = engine
        self.member_number = engine.get_member_number()
        pass
    
    @abstractmethod
    def generate_schluempfe(self):
        return []

class Schlumpf(ABC):
    """"
    This is an abstract class for the Schlumpf interface.
    
    Parameter:
    internal_id (int): 'Tell them their name' by giving them a int number
    current_game (GameEngine): give them the reference to the active GameEngine so a Schlumpf knows their context
    
    It's interface is
    get_id() – returns Schlumpf's ID
    inspect_lamp() – when in interrogation room, yields the status of the lamp
    invert_lamp() – flips the lamp status
    ask_question() – corresponds to the specific action of sking the ultimate question when certain conditions are fulfilled
    stay_quiet() – corresponds to actions involving not asking the ultimate question.
    
    get_response () – only called by the game_engine; 
    """
    
    def __init__(self, internal_id: int, current_game: None):
        self.internal_id = internal_id
        self.current_game = current_game
        
        
        self.been_drawn = 0 #remembers how many times they have been to the interrogation room
        self.count_schluempfe = 0 #a counting variable that may correspond to different counting methods
        self.toggled_lamps = 0 #corresponds to the amount of times they have toggled the lamp
        
        self.memory_toggled_lamps = [] #corresponds to how when they have individually toggled the lamp
        self.memory_lamp_status_on_entrance= []
        self.memory_lamp_status_when_leaving = []
        pass
    
        
    def get_id(self) -> int:
        return self.internal_id
    
    def _inspect_is_lamp_active_(self) -> bool:
        return self.current_game.is_lamp_active()
    
    def _invert_lamp_(self) -> bool:
        self.current_game.invert_lamp()
    
    
    #
    # These two methods may seem redundant
    # However, they are semantically important
    # as they encode the meaning behind "staying quiet" and "asking the question"
    # generally
    # Additionally,
    # some special role may want a different behaviour here
    #
    def _ask_question_(self):
        return True
    
    def _stay_quiet_(self):
        return False
    
    @abstractmethod
    def get_response(self):
        self.been_drawn += 1
        self.memory_lamp_status_on_entrance.append(self._inspect_lamp_)   
   
class GameEngine:
    """
    GameEngine Class represents Gargamel's behaviour, providing
    the number of schlumpfs put into cells,
    as well as the lamp status. Furthermore, GameEngine remembers 
    every Schlumpf brought into the interrogation room
    and is calling the individual Schlumpf Objects.
    
    Parameters:
    member_number (int): number of how many Schlumps are brought into the game (in our example it's been 100).
    
    Methods:
    start() - starts the game and returns its result (False = Schlümpfe have won; True = Gargamel has won)
    
    """
    
    def __init__(self, member_number: int):
        
        try:
            self.member_number = member_number
            if member_number == 0:
                raise ValueError(f"{member_number} Schlümpfe macht keinen Sinn")
        except ValueError as e:
            print(f"Fehler: ", e, " proceed with 1 Schlumpf")
            self.member_number = 1 #This is nasty card coded exception management
            
        #except ValueError as e: #do not catch so this would break the program run
        #    print("Fehler: ", e)
            
            
        self.steps = 0
        self.schlumpf_memory = []
        self.schlmpfs = []
        self.lamp_active = False
        self.game_ended = False
        self.gargamel_won = None
        
        context = GameContext()
        context.set_engine(self) #Latest GameEngine object initialized defines context
        
        #self.schluempfe = [Lemming(i, self) for i in range (member_number-1)]
        #self.schluempfe.append(Decider(member_number-1, self))
       
    def start(self, str: Strategy) -> bool:
        """
        Starts the game and returns its result (False = Schlümpfe have won; True = Gargamel has won)
        """
        
        try:
            self.schlmpfs = str.generate_schluempfe()
            if len(self.schlmpfs) != self.member_number:
                raise ValueError(f"Strategie hat falsche Schlumpf-Anzahl generiert: {len(self.schlmpfs)}, erwartet werden {self.member_number}.")
            
        except ValueError as e:
            print("Fehler: ", e)
        #We could flag RunTimeErrors here as well when strategy leads to not terminating runtime error. However not limiting strategy approaches, it is difficult to define when to abort (N^2 steps? N^2.5 steps? for e.g. probablistic solution?)
        
        while not self.game_ended:
            self._draw_next_()
        
        return self._get_simulation_result_()
        #self._reset_() #from old approach
        
   
    
    
    
    def _draw_next_(self) -> bool:
        self.steps += 1
        #print(f"Step Nr. {self.steps}")
        
        #Draw a random Schlumpf:
        schlumpf_id = random.randint(0, self.member_number)
        
        #Remember its id:
        if(self.schlmpfs[schlumpf_id].get_id() not in self.schlumpf_memory):
            self.schlumpf_memory.append(self.schlmpfs[schlumpf_id].get_id())
    
        #
        # Draw the Schlumpf into interrogation room und see what they do.
        # Act accordingly: if you get a response, end the game.
        # Otherwise, draw next Schlumpf.
        #
        
        if(self.schlmpfs[schlumpf_id].get_response()):
            return self._end_()
        else:
            return False
  
    #    
    # Internal get() Functions - for readability, may be shrinked down
    # as they also make reading more complex
    #
    def _is_lamp_active_(self) -> bool:
        return self.lamp_active
        
    def _get_member_number_(self) -> int:
        return self.member_number
    
    def _get_schlumpf_id_(s: Schlumpf) -> int:
        return s.get_id()
    
    def _get_simulation_result_(self):
        result = self.gargamel_won
        self._reset_()    
        return result
    
    #
    #
    #
    def _invert_lamp_(self) -> None:
        """
        Flips the status of the lamp
        
        Internal functions. External calls only through GameContext object
        
        """
        if(self.lamp_active):
            self.lamp_active = False
        else:
            self.lamp_active = True
    
    def _end_(self) -> bool:
        """
        Returns if game run has ended (only callable by internal methods)
        Decide what to do. 
        If every Schlumpf was to the interrogation room, set them free.
        
        """
        if(len(self.schlumpf_memory) == self.member_number):
           print(f"### Die Schlümpfe haben überlebt! ###")
           self.gargamel_won = False
           self.game_ended = True
           return True
       #Otherwise, kill 'em all:
        else:
           print(f"### Gargamel bringt nun alle Schluempfe um! ###")
           self.gargamel_won = True
           self.game_ended = True
           return True
    
    def _reset_(self):
            self.steps = 0
            self.schlumpf_memory = []
            self.schlmpfs = []
            self.lamp_active = False
            self.game_ended = False
            self.gargamel_won = None
            
class GameContext:
    """
    Produces singleton object providing context calls
    
    -> Both Schlümpfe as well as our Strategy Class needs context information.
       In order to make the GameEngine object free of undesired behavior
       let's encapsulate that information (as it is nothing more but that)
       into a singleton GameContext
    
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameContext, cls).__new__(cls)
            cls._instance.engine = None
        return cls._instance
    
    def set_engine(self, engine):
        """
        Changes active engine to engine passed by parameter
        (for cases where several game engine make sense, 
        functionality is already implemented)
        """
        self.engine = engine
    
    def is_lamp_active(self) -> bool:
        """
        Gets GameEngine object's lamp_status
        """
        return self.engine._is_lamp_active_()
    
    def invert_lamp(self):
        """
        Inverts GameEngine object's lamp_status
        """
        self.engine._invert_lamp_()
    
    def get_member_number(self) -> int:
        """
        Gets GameEngine object's member_number
        """
        return self.engine._get_member_number_()