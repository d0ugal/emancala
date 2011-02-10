from pycala.players import basic
from pycala.engine import tournament
from pycala.engine import players

number_of_each = 4
max_depth = 4

PLAYER_LIST = []

random_bases = []
for x in range(0,number_of_each):
    random_bases.append(basic.MiniMaxPlayer.objects.random(name="M2%s" %x, settings={'max_depth':1,}))
    random_bases.append(basic.MiniMaxPlayer.objects.random(name="M2%s" %x, settings={'max_depth':1,}))

for i in range(100):
    r = players.ConfiguredPlayer(basic.RandomPlayer, name="R %s" %i,)
    PLAYER_LIST.append(r)

for y in range(1,max_depth+1):
    for i in range(0,number_of_each):
        mm = basic.MiniMaxPlayer.objects.random(name="M%s%s" %(y,i), weights=random_bases[i].weights, settings={'max_depth':y,})
        PLAYER_LIST.append(mm)

mt = tournament.MancalaTournament(PLAYER_LIST)
mt.VERBOSE = True
mt.run()
sb = mt.score_board()

for c in sb:
    print c
