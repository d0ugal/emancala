# Not very cool, but disables a warning caused by the MySQLdb module.
import warnings
warnings.filterwarnings("ignore")

from sys import stdout

from pycala import engine
from pycala.engine import board
from pycala.engine import players
from pycala.players import basic
from pycala.players.nn.player import NeuralNetPlayer
from pycala.players.nn.models import Neuron, Log

class NeuralNetwork(object):
    
    def __init__(self, propogation_decay=0.95,):
        
        self.serializer = board.BoardSerializer()
        self.propogation_decay = propogation_decay
    
    def train(self, configured_players, repeat=1):
        
        for i in range(repeat):
            
            sum = 0
            
            for cp in configured_players:
                r = self._train(cp)
                print r[0], "\t", r[1], "(%s)"%cp.name
                sum += r[0]
            
            print ""
            
            if sum <= 0:
                print "  %s" % sum
            else:
                print "  %s\t <----" % sum
        
    def _train(self, cp):
        
        nn_player = players.ConfiguredPlayer(NeuralNetPlayer, name="NNN")
        
        #print nn_player.name, "vs", cp.name, "--",
        
        home_game = board.MancalaGame(nn_player, cp)
        home_game.run_game()
        home_a, home_b = home_game.board.scores()
        self.backpropogate(home_game)
        
        result = (0,'###',)
        
        if home_a > home_b:
            #print '%02s %02s -- NN' % (home_a, home_b)
            result = (1,nn_player.name,)
            Log(result=1).save()
        elif home_b > home_a:
            #print '%02s %02s -- CP' % (home_a, home_b)
            result = (-1,cp.name,)
            Log(result=-1).save()
        else:
            #print '%02s %02s -- DR' % (home_a, home_b)
            Log(result=0).save()
            pass
        
        return result
    
    
    def _update_neuron(self, binary, value, end_game):
        
        n, created = Neuron.objects.get_or_create(binary=binary)
        
        if end_game.board.game_result == engine.GAME_WON_A:
            n.won += 1
        elif end_game.board.game_result == engine.GAME_WON_B:
            n.lost += 1
        else:
            n.draw += 1
        
        n.probability += value
        n.save()
    
    def backpropogate(self, end_game):
          
        if end_game.board.game_state != engine.GAME_FINISHED:
            raise Exception, "Learning from an unfinished game?!"
        
        history = end_game.board.game_history[:]
        history.reverse()
        
        
        
        if end_game.board.game_result == engine.GAME_WON_A:
            value = -2.0
        elif end_game.board.game_result == engine.GAME_WON_B:
            value = 1
        else:
            value = 0
        
        end_game_binary = self.serializer.as_binary(end_game.board)
        
        n, created = Neuron.objects.get_or_create(binary=end_game_binary)
        
        if created and n.end_visited:
            return
        
        n.end_visited = True
        n.save()
        
        self._update_neuron(end_game_binary, value, end_game)
        
        for past_board in history:
            
            value *=self.propogation_decay
            
            binary = self.serializer.as_binary(past_board)
            
            self._update_neuron(binary, value, end_game)

class NeuralNetworkAway(NeuralNetwork):

    def _train(self, cp):
        
        nn_player = players.ConfiguredPlayer(NeuralNetPlayer, name="NNN")
        
        #print nn_player.name, "vs", cp.name, "--",
        
        home_game = board.MancalaGame(cp, nn_player)
        home_game.run_game()
        home_a, home_b = home_game.board.scores()
        self.backpropogate(home_game)
        
        result = (0,'###',)
        
        if home_a < home_b:
            #print '%02s %02s -- NN' % (home_a, home_b)
            result = (1,nn_player.name,)
            Log(result=1).save()
        elif home_b < home_a:
            #print '%02s %02s -- CP' % (home_a, home_b)
            result = (-1,cp.name,)
            Log(result=-1).save()
        else:
            #print '%02s %02s -- DR' % (home_a, home_b)
            Log(result=0).save()
            pass
        
        return result

class NeuralNetworkBoth(NeuralNetwork):

    def train(self, configured_players, repeat=1):
        
        for i in range(repeat):
            
            sum = 0
            
            for cp in configured_players:
                r = self._train(cp)
                print r[0][0], "\t", r[0][1], "(%s)"%cp.name
                sum += r[0][0]
                print r[1][0], "\t", r[1][1], "(%s)"%cp.name
                sum += r[1][0]
            
            print ""
            
            if sum <= 0:
                print "  %s" % sum
            else:
                print "  %s\t <----" % sum

    def _train(self, cp):
        
        nn_player = players.ConfiguredPlayer(NeuralNetPlayer, name="NNN")
        
        #print nn_player.name, "vs", cp.name, "--",
        
        home_game = board.MancalaGame(cp, nn_player)
        home_game.run_game()
        home_a, home_b = home_game.board.scores()
        self.backpropogate(home_game)
        
        result = []
        
        if home_a < home_b:
            #print '%02s %02s -- NN' % (home_a, home_b)
            result.append((1,nn_player.name,))
            Log(result=1).save()
        elif home_b < home_a:
            #print '%02s %02s -- CP' % (home_a, home_b)
            result.append((-1,cp.name,))
            Log(result=-1).save()
        else:
            #print '%02s %02s -- DR' % (home_a, home_b)
            Log(result=0).save()
            result.append((0,'###',))
            
        home_game = board.MancalaGame(nn_player, cp)
        home_game.run_game()
        home_a, home_b = home_game.board.scores()
        self.backpropogate(home_game)
        
        if home_a > home_b:
            #print '%02s %02s -- NN' % (home_a, home_b)
            result.append((1,nn_player.name,))
            Log(result=1).save()
        elif home_b > home_a:
            #print '%02s %02s -- CP' % (home_a, home_b)
            result.append((-1,cp.name,))
            Log(result=-1).save()
        else:
            #print '%02s %02s -- DR' % (home_a, home_b)
            Log(result=0).save()
            result.append((0,'###',))
        
        return result