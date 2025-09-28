import sys
import os

import pytest
from unittest.mock import Mock, patch

from classes import Strategy, GameEngine, Schlumpf, GameContext
from schluempfe import Decider, Lemming, OptimalStrategy, HopeForGod

"""
Here are some unit and integration tests
They are incomplete but convey the idea
"""

class TestGameEngine:
    """
    Some Tests for GameEngine class
    """
    
    def setup_method(self):
        """
        Simple setup
        """
        self.game = GameEngine(5)  
    
    def test_initialization(self):
        """
        Test if initialization works as expected
        """
        assert self.game.member_number == 5
        assert self.game.steps == 0
        assert self.game.lamp_active == False
        assert self.game.game_ended == False
        assert self.game.gargamel_won is None
        assert len(self.game.schlumpf_memory) == 0
    
    def test_get_member_number_(self):
        
        assert self.game._get_member_number_() == 5
        
        # Try another example
        game2 = GameEngine(100000)
        assert game2._get_member_number_() == 100000
    
    def test_lamp_operations(self):
        # Initially lamp is off
        assert self.game._is_lamp_active_() == False
        
        # Invert lamp, has to be On
        self.game._invert_lamp_()
        assert self.game._is_lamp_active_() == True
        
        # Invert lamp again, should be off
        self.game._invert_lamp_()
        assert self.game._is_lamp_active_() == False
    
    def test_end_game_all_visited(self):
        """
        Test if game ends accordingly 
        after all schlumps have been  drawn
        """
        # Simulation
        self.game = GameEngine(5)
        self.game.schlumpf_memory = [0, 1, 2, 3, 4]
        
        result = self.game._end_()
        
        assert result == True
        assert self.game.game_ended == True
        assert self.game.gargamel_won == False 
    
    def test_end_game_not_all_visited(self):
        """
        Tests if game ends accordingly
        after not all schlumpfs have been drawn
        """
        # Simulation
        self.game.schlumpf_memory = [0, 1, 2]
        
        result = self.game._end_()
        
        assert result == True
        assert self.game.game_ended == True
        assert self.game.gargamel_won == True

class TestGameContext:
    """
    Testing singleton GameContext
    """
    
    def test_singleton_behavior(self):
        """test if it's really a singelton"""
        context1 = GameContext()
        context2 = GameContext()
        
        assert context1 is context2  
    
    def test_engine_setting(self):
        """test if its setting engine correctly"""
        mock_engine = Mock()
        context = GameContext()
        
        context.set_engine(mock_engine)
        
        assert context.engine is mock_engine

class TestOptimalStrategy:
    """Tests für die OptimalStrategy"""
    
    def setup_method(self):
        """Setup für jeden Test"""
        self.mock_engine = Mock()
        self.mock_engine.get_member_number.return_value = 5
        self.strategy = OptimalStrategy(self.mock_engine)
    
    def test_generate_schluempfe(self):
        """Testet ob die richtige Anzahl und Typen von Schlümpfen generiert werden"""
        schluempfe = self.strategy.generate_schluempfe()
        
        assert len(schluempfe) == 5
        
        # Ersten 4 sollten Lemmings sein
        for i in range(4):
            assert isinstance(schluempfe[i], Lemming)
            assert schluempfe[i].get_id() == i
        
        # Letzter sollte Decider sein
        assert isinstance(schluempfe[4], Decider)
        assert schluempfe[4].get_id() == 4

"""
Could also do unit tests on Decider, Lemming, HopeForGod Schlumpf
"""
class TestIntegration:
    """
    Test some GameEngine situations
    """
    
    #Test if it successfully leads to Schlumpf win
    @patch('numpy.random.randint')
    @patch.object(GameEngine, '_reset_') #do nothing
    def test_game_schluempfe_win(self, mock_reset, mock_randint):
        """ 
        Test some situation where Gargamel wins
        """
        mock_randint.side_effect = [0, 4, 1, 4, 2, 4, 3, 4]  # Schlumpf ID how they now are being drawn
        
        game = GameEngine(5)
        
        context = GameContext()
        context.set_engine(game)
        
        strategy = OptimalStrategy(context) #just pass actual Game Engine as context
        
        
        game.start(strategy)  
       
        assert game.gargamel_won == False
        assert len(game.schlumpf_memory) == 5


def find_all_subclasses(base_class):
    return base_class.__subclasses__()


def test_all_schlumpf_subclasses_implement_correct_response():
    """
    Test if:
    Every Schlumpf subclass implements overriden
    get_response() method. 
    """
    
    subclasses = find_all_subclasses(Schlumpf)
    
    for subclass in subclasses:
        # ... Mock GameEngine
        mock_game = Mock()
        mock_game.get_member_number.return_value = 5
        
        # create instance of sub class object
        instance = subclass(1, mock_game)
        
        # Set ask/stay methods for simpler tracking
        instance._ask_question_ = Mock(return_value=True)
        instance._stay_quiet_ = Mock(return_value=False)
        
        # Call get_response 
        result = instance.get_response()
        
        # Check if either _ask_question_ or _stay_quiet_ have been called
        ask_called = instance._ask_question_.called
        stay_called = instance._stay_quiet_.called
        
        assert ask_called or stay_called, f"{subclass.__name__} ruft weder _ask_question_ noch _stay_quiet_ auf"
        
def test_all_strategy_subclasses_return_list():
    """
    Test if:
    Every strategy sub class returns a list 
    
    Better: a list with schlumpfs matching member_number, but for now it takes to long to implement as
    in practice you could just implement a specific case and have no reason for implementing
    a general case    
    """
    
    subclasses = find_all_subclasses(Strategy)
    
    for subclass in subclasses:
        
        mock_engine = Mock()
        mock_engine.get_member_number.return_value = 5
        
        strategy = subclass(mock_engine)
        
        # Generiere Schlümpfe
        schluempfe = strategy.generate_schluempfe()
        
        # Prüfe dass eine Liste zurückgegeben wird
        assert isinstance(schluempfe, list), \
            f"{subclass.__name__}.generate_schluempfe() gibt keine Liste zurück"


# Fixtures für wiederverwendbare Test-Objekte

class TestEdgeCases:
    """
    Test some Edge Cases
    """
    
    def test_optimal_game_with_one_member(self):
        """
        Test what happens for N=1
        """
        game = GameEngine(1)
        strategy = OptimalStrategy(GameContext())
        schluempfe = strategy.generate_schluempfe()
        
        assert len(schluempfe) == 1
        assert isinstance(schluempfe[0], Decider)  # Should be decider in this case
    
    
   


if __name__ == "__main__":
    pytest.main([__file__, "-v"])