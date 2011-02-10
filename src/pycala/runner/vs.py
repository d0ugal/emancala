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


from pycala.players.basic import MiniMaxPlayerExplorer as MM
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

w = {'pit9': 0.21357042541093296, 'pit8': 0.27622735612420146, 'pit1': -0.057235318739945709, 'pit0': -0.10277322535894143, 'pit3': 0.29064588660661039, 'pit2': -0.28573261991208698, 'pit5': -0.63808960652959767, 'pit4': -0.53494882216118422, 'pit7': -0.31548979107649761, 'pit6': 0.40242859243812173, 'pit11': 0.097991320786572245, 'pit10': -0.29838914087039992, 'pit13': -0.63035595843416337, 'pit12': 0.15773912935388326}

mm = ConfiguredPlayer(MM, weights=w, settings=s, name="MM")
hp = ConfiguredPlayer(HumanPlayer, name="HP")

mt = MancalaTournament([mm,hp,], verbose=True)

mt.run(play_self=False)