from pycala.players.nn.models import Neuron
from pycala.engine import board
from pycala.engine import players
from pycala import engine

b = board.MancalaBoard()
s = board.BoardSerializer()

neuron_list = []

second_level = {}

for turn in b.get_possible_turns():
    tmp_board = b.move(turn)
    second_level[str(turn)] = tmp_board
    binary = s.as_binary(tmp_board)
    n,created = Neuron.objects.get_or_create(binary=binary)
    neuron_list.append({'turn':turn,'binary':binary, 'probability':round(n.probability,7),
                        'won':n.won,'lost':n.lost, 'draw':n.draw,})

print "\n\nturn\tprobability\twon\tWon_p\tlost\tlost_p\tdrawn\tdrawn_p"
for n in neuron_list:
    total = float(n['won']) + float(n['lost']) + float(n['draw'])
    won_p = round(n['won']/total * 100,2)
    lost_p = round(n['lost']/total * 100,2)
    drawn_p = round(n['draw']/total * 100,2)
    print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (n['turn'], n['probability'], n['won'], won_p, n['lost'], lost_p, n['draw'], drawn_p)

second_level_neurons = []

print "\nBest Counter Moves!"
for prev_turn in second_level:
    board = second_level[prev_turn]
    for turn in board.get_possible_turns():
        tmp_board = board.move(turn)
        binary = s.as_binary(tmp_board)
        n,created = Neuron.objects.get_or_create(binary=binary)
        second_level_neurons.append({'turn':turn,'prev_turn':prev_turn,'binary':binary, 'probability':round(n.probability,7),
                            'won':n.won,'lost':n.lost, 'draw':n.draw,})

second_level_neurons = sorted(second_level_neurons, key=lambda x:-x['probability'])
second_level_neurons = sorted(second_level_neurons, key=lambda x:str(x['prev_turn']))

print "\n\nturn\tprobability\twon\tWon_p\tlost\tlost_p\tdrawn\tdrawn_p"
for n in second_level_neurons:
    total = float(n['won']) + float(n['lost']) + float(n['draw'])
    won_p = round(n['won']/total * 100,2)
    lost_p = round(n['lost']/total * 100,2)
    drawn_p = round(n['draw']/total * 100,2)
    print "%s\t%10s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (n['prev_turn'], n['turn'], n['probability'], n['won'], won_p, n['lost'], lost_p, n['draw'], drawn_p)