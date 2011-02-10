from pycala.engine import tournament
from pycala.engine import players
from pycala.players import basic

player_list = []

for i in xrange(10):
    #player_list.append(players.ConfiguredPlayer(basic.RandomPlayer, name="R%03s"%i))
    player_list.append(basic.MiniMaxPlayer.objects.random(name="M%03s"%i, settings={'max_depth':3,}))
    
settings={'max_depth':3,}
weights=weights={'scrape':100.0, 'store':10.0, 'score':0.5, 'stance':0.0, 'pits_multi':[10.0,9.0,8.0,7.0,6.0,5.0],}
cro = players.ConfiguredPlayer(basic.MiniMaxPlayer, weights, settings=settings, name="MMCC")
player_list.append(cro)

t = tournament.MancalaTournament(player_list)

r = t.run(yield_length=True)

l = list(r)



print sum([len(i) for i in l])/len(l)
print max([len(i) for i in l])
print min([len(i) for i in l])

games = l[0]

for game in games:
    print game.board
    import time
    time.sleep(10)