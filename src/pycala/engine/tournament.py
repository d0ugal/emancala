import sys

from pycala import engine
from pycala.engine import board

class MancalaTournament(object):
    
    def __init__(self, players, verbose=False):
        self.VERBOSE = verbose
        
        self.players = players
    
    def run(self, *args, **kwargs):
        return list(self._run(*args, **kwargs))
    
    def _run(self, games=1, reset=True, play_self=True, yield_length=False):
        
        if reset:
            for player in self.players:
                player.win = []
                player.lost = []
                player.drawn = []
                player.for_points = 0
                player.away_points = 0
        
        # added 1 so we never say 'Playing game 0'
        num_games = ((len(self.players)*len(self.players))*games)+1
        
        if not play_self:
            num_games -= (games *2)
        
        for player_a in self.players:
            for player_b in self.players:
                for i in xrange(0,games):
                    if not play_self and player_a == player_b:
                        continue # lets not bother playing ourselves!
                    
                    if getattr(self, 'VERBOSE', False):
                        print player_a.name, 'vs', player_b.name
                        
                    if getattr(self, 'VERBOSE', False):
                        mg = board.MancalaGame(player_a, player_b, verbose=True)
                    else:
                        mg = board.MancalaGame(player_a, player_b)
                        
                    mg.run_game()
                    
                    a_score, b_score = mg.board.scores()
                    
                    mg.conf_player_a.for_points += a_score
                    mg.conf_player_a.away_points += b_score
                    mg.conf_player_b.for_points += b_score
                    mg.conf_player_b.away_points += a_score
                    
                    if yield_length:
                        yield mg.board.game_history
                    
                    if getattr(self, 'VERBOSE', False):
                        print "(%02s, %02s)" % mg.board.scores()
                    
                    if mg.board.game_result == engine.GAME_WON_A:
                        mg.conf_player_a.won.append(mg.conf_player_b)
                        mg.conf_player_a.home_won += 1
                        mg.conf_player_b.lost.append(mg.conf_player_a)
                        mg.conf_player_b.away_lost += 1
                    elif mg.board.game_result == engine.GAME_WON_B:
                        mg.conf_player_b.won.append(mg.conf_player_a)
                        mg.conf_player_b.away_won += 1
                        mg.conf_player_a.lost.append(mg.conf_player_b)
                        mg.conf_player_a.home_lost += 1
                    else:
                        mg.conf_player_a.drawn.append(mg.conf_player_b)
                        mg.conf_player_b.drawn.append(mg.conf_player_a)
        
    def winner(self, method='difference', second=None):
        return self.score_board(method, second)[0]
    
    def score_board(self, method='difference', second=None):
        
        def score(obj):
            return obj.points(method=method)
        
        def second_sort(obj):
            return obj.points(method=second)
        
        s = sorted(self.players, key=score, reverse=True)
        
        if second:
            return sorted(s, key=second_sort, reverse=True)
        return s
    
    def stats(self):
        pass