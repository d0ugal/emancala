from pycala.players import basic
from pycala.engine import tournament
from pycala.engine import players

number_of_each = 10
max_depth = 4

PLAYER_LIST = []

random_bases = []
for x in range(0,number_of_each):
    random_bases.append(basic.MiniMaxPlayer.objects.random(name="M2%s" %x, settings={'max_depth':1,}))
    random_bases.append(basic.MiniMaxPlayer.objects.random(name="M2%s" %x, settings={'max_depth':1,}))

for i in range(30):
    r = players.ConfiguredPlayer(basic.RandomPlayer, name="R%02s" %i,)
    PLAYER_LIST.append(r)

for y in range(1,max_depth+1):
    for i in range(0,number_of_each):
        mm = basic.MiniMaxPlayer.objects.random(name="M%s%s" %(y,i), weights=random_bases[i].weights, settings={'max_depth':y,})
        PLAYER_LIST.append(mm)

c_mm = players.ConfiguredPlayer(basic.MiniMaxPlayer,weights={'scrape':100.0, 'store':10.0, 'score':0.5, 'stance':0.0, 'pits_multi':[10.0,9.0,8.0,7.0,6.0,5.0],}, settings={'max_depth':1,}, name="MC1",)
PLAYER_LIST.append(c_mm)
c_mm = players.ConfiguredPlayer(basic.MiniMaxPlayer,weights={'scrape':100.0, 'store':10.0, 'score':0.5, 'stance':0.0, 'pits_multi':[10.0,9.0,8.0,7.0,6.0,5.0],}, settings={'max_depth':2,}, name="MC2",)
PLAYER_LIST.append(c_mm)
c_mm = players.ConfiguredPlayer(basic.MiniMaxPlayer,weights={'scrape':100.0, 'store':10.0, 'score':0.5, 'stance':0.0, 'pits_multi':[10.0,9.0,8.0,7.0,6.0,5.0],}, settings={'max_depth':3,}, name="MC3",)
PLAYER_LIST.append(c_mm)
c_mm = players.ConfiguredPlayer(basic.MiniMaxPlayer,weights={'scrape':100.0, 'store':10.0, 'score':0.5, 'stance':0.0, 'pits_multi':[10.0,9.0,8.0,7.0,6.0,5.0],}, settings={'max_depth':4,}, name="MC4",)
PLAYER_LIST.append(c_mm)

mt = tournament.MancalaTournament(PLAYER_LIST)
mt.VERBOSE = True
mt.run()
sb = mt.score_board()


for c in sb:
    print c
    
print "\n\nWinner", mt.winner()
print "\n", mt.winner().weights
