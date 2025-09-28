# Schlumpfproblem - Simulationstool

## Idee
Das Programm testet Strategien für das "Schlumpfproblem" und führt diese konkret aus.
Weiter stellt es ein einfaches Framework bereit, um eine beliebige Strategie zu definieren und zu testen.

## Usage
1. In main(), you define a game object like game = GameEngine(100) to let Gargamel capture 100 Schlümpfe.
Now you have implemented Gargamel's part of the problem.

2. Then, in e.g. define_strategy.py, it is your turn to define a strategy.
a) For that, define Schlumpf Roles by inheriting Schlumpf Class. Keep in mind to override get_reponse() method and at least call _stay_quiet()_ there.
b) After that, you define a strategy class for your strategy. Here, you override get_schluempfe() method and keep in mind to match the Number of Schlümpfe captured. Keep also in mind when initializing your Schlümpfe, to pass them both an int id as well as the GameContext like: schlmpf = YourSchlumpf(0, GameEngine())

3. In main(), you initialize your strategy object by calling str = YourStrategy(GameContext()). GameContext() corresponds to a singelton object keeping all the important information at hand.

4. Now, everything is ready! Call game.start(str) (you pass your strategy object as parameter) und see if your strategy helps them or leads them to death! 


## Classes
class GameEngine:
	Represents Gargamels behaviour and offers relevant information to subclasses.
	Has to be initialized as object in main function to load game functionality.

	Parameters:
		member_number: int
		Represents of Schlumpfs being catched by Gargamel

	Public Methods:
		start(str: Strategy) -> bool:
		Takes a certain Strategy object as parameter. Starts simulation and returns its termination status as bool:
		False = simulation ongoing
		True = simulation has terminated

class GameContext:
	Represents singelton object so that
	information about game status
	may be send to external functions without
	creating potentially undesired behaviours
	
	Parameters:
		None
	Public Methods:
		
		set_engine(self, engine):
		Takes a (GameEngine) object as Parameter
		and sets that as GameContext reference.
		
		get_lamp_status(self)->bool:
		Returns lamp status in corresponding GameEngine object
		
		invert_lamp(self):
		Inverts GameEngines Lamp status in corresponding GameEngine object
		
		get_member_number(self)->int:
		Returns number of Schlumpfs captured by Gargamel in corresponding GameEngine object.

class Strategy:
	Abstract strategy class ready to implement your strategy.
	
	Parameters:
	engine: GameContext
	Sets reference to the GameContext at hand
	
	generate_schluempfe():
	Generates Schlümpfe and returns list full of them.
	Needs to be overriden in your Strategy Class inheriting from Strategy.
	
class Schlumpf:
	This is an abstract class for the Schlumpf interface.
    
 	Parameter:
    internal_id (int): 'Tell them their name' by giving them a int number
    current_game (GameContext): give them the reference to the active GameEngine so a Schlumpf knows their context
    
    internally:
    self.been_drawn = 0
    Remembers how many times they have been to the interrogation room
    self.count_schluempfe = 0 
    Acounting variable that may correspond to different counting methods
     self.toggled_lamps = 0
     Another counting variable that may correspond to the amount of times they have toggled the lamp
        
       self.memory_toggled_lamps = [] 
       List that may orrespond to a memory on what pull into interrogation room they have individually toggled the lamp
       self.memory_lamp_status_on_entrance= []
       List that may correspond to a memory on what pull into interrogation room they have encounterd which lamp status 
        self.memory_lamp_status_when_leaving = []
       List that may correspond to a memory on lamp status in interrogation room when they leave 
       
    Public Methods:
    get_id()->int: – returns Schlumpf's ID
    get_response() – only called by the GameEngine. Defines behavíour when drawn to interrogation room. Has to be overriden when inheriting from Schlumpf class and HAS to implemetn at least _stay_quiet_() method. 
    
    Private Methods
   	 _inspect_lamp_()):
   	 	when in interrogation room, yields the status of the lamp
    _invert_lamp_(): 
      flips the lamp status
    _ask_question_():
    	corresponds to the specific action of sking the ultimate question when certain conditions are fulfilled
    _stay_quiet_():
    	 corresponds to actions involving not asking the ultimate question.
    
	

-