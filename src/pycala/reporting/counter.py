import time
import random
import datetime
import os
from multiprocessing import cpu_count, Process, Pool, Queue 

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from pycala import GRAPH_STORE
from pycala import engine
from pycala.engine import board
from pycala.players import basic

def node_counter(args):
    
    working_board = args[0]
    depth = args[1]
    
    start = time.time()
    output = ""
    
    counts = [1 for i in xrange(1,depth+2)]
    
    for i in xrange(1,depth+1):
        settings = {'max_depth':i,}
        conf_mm = basic.MiniMaxPlayer.objects.random(settings=settings)
        working_board.set_turn(engine.PLAYER_B)
        mm = conf_mm.create(working_board.whos_turn())
        result = mm.get_move(working_board)
        
        working_board.move(pits=result,)
        
        counts[i] = sum(mm.nodes_at_depth)
        
        output += "D:%s N:%s\t" % (i, sum(mm.nodes_at_depth))
    
    total = round(time.time() - start, 2)
    
    print "STONES:%s -" % working_board.stones,
    print output,
    print "(%s seconds)" % total
    
    return { working_board.stones : counts}
    
if __name__ == '__main__':
    
    for d in xrange(1,5):
        
        start_start = time.time()
        
        cpus = cpu_count()
        
        pool = Pool(processes=cpus)
        
        boards = [[board.MancalaBoard(stones=i),d,] for i in xrange(1,9)]
        
        results = pool.map(node_counter, boards)
    
        print time.time() - start_start, "s"
        
        for s in xrange(1,7):
            
            fig = Figure()
            
            sub_results = results[:s]
        
            for result in sub_results:
                
                ax = fig.add_subplot(111)
                ax.set_xlabel('Search Depth')
                ax.set_ylabel('Node Count')
                ax.set_title('y Nodes at x Depth with z stones')
                x = []
                y = []
                y_c = 0
                for i in result.get(result.keys()[0]):
                    
                    y.append(i)
                    x.append(y_c)
                    y_c += 1
                
                ax.set_xticks([i for i in xrange(len(x))], minor=False)
                
                l1 = ax.plot(x,y,'-', label='%s Stones' % result.keys()[0])
                
                ax.legend(loc='upper left')
            
            canvas=FigureCanvas(fig)
            
            filename = str(os.path.join(GRAPH_STORE, 'counter', 'Depth %s Stones %s.png' % (d,s),))
            
            fig.savefig(filename, dpi=300)    