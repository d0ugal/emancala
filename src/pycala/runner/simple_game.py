import sys

class Unbuffered:
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)
    
sys.stdout=Unbuffered(sys.stdout)


from pycala.players.basic import MiniMaxPlayer as MM
from pycala.players.basic import HumanPlayer
from pycala.engine.tournament import MancalaTournament
from pycala.engine.players import ConfiguredPlayer

s = {'max_depth':3,}
#w = {'pit9': -0.37588174149363462,  'pit8': 0.085305102426567525, 
#     'pit1': -0.029707060382366313, 'pit0': 0.033970872974465521, 
#     'pit3': 0.6507764164079789,    'pit2': -0.31106442059016215, 
#     'pit5': -0.030329220000473018, 'pit4': -0.35227307760479265, 
#     'pit7': -0.13693598484925443,  'pit6': 0.37972050557341219, 
#     'pit11': 0.3393923402316788,   'pit10': -0.28953360804226114, 
#     'pit13': -0.60567631158989654, 'pit12': -0.43406889724758213,}

w = {'pits_multi': [-0.65176288138525651, -0.55627229002391476, 0.19739760963451791, -0.036389123108288901, 0.74305046637027683, -0.58737509070641414], 'score': 0.12763495825805615, 'store': 0.66761402951468951, 'stance': -0.07376975759431903, 'scrape': -0.56479132567225676}

mm = ConfiguredPlayer(MM, weights=w, settings=s, name="MM")
hp = ConfiguredPlayer(HumanPlayer, name="HP")

mt = MancalaTournament([mm,hp,])

mt.run(play_self=False)