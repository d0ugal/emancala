# Not very cool, but disables a warning caused by the MySQLdb module.
import warnings
warnings.filterwarnings("ignore")

# While this isn't directly used, this must be included as it sets up
# django's settings path etc.
from pycala.players.nn.models import Neuron

# Get the database connection from django
from django.db import connection
cursor = connection.cursor()

import locale
locale.setlocale(locale.LC_ALL, '')

# Counts the total number of Neurons currently in the net and the number
# of visits made. Where a visit is each time a neuron has been activated
# This allows for an interesting analysis of the data as its possible
# to see the most frequently visited neurons, while some may be obvious
# (i.e. the starting positions) it could highlight the most common end
# game scenarios.
cursor.execute("""
    SELECT 
        COUNT(visited) as 'Total Neurons' , 
        SUM(visited) as 'Total visits' 
    FROM nn_neuron
""")
totals = cursor.fetchone()

# Counts various statistis, all fairly self explanitor.
# These are;
#    Total Games
#    Score - SUM of result where win=1, draw=0, lost=-1
#    Won and Won Percentage
#    Drawn and Drawn Percentage
#    Lost and Lost Percentage
#    AVG Neurons per Game
cursor.execute("""
    SELECT 
        COUNT(result) 'Total Games', 
        SUM(result) as 'Score', 
        (SELECT COUNT(result) FROM nn_log WHERE result = 1) as 'Won', 
        (SELECT COUNT(result) FROM nn_log WHERE result = 1)/COUNT(result)*100 as 'Won Percentage',
        (SELECT COUNT(result) FROM nn_log WHERE result = '0') as 'Drawn', 
        (SELECT COUNT(result) FROM nn_log WHERE result = '0')/COUNT(result)*100 as 'Drawn Percentage', 
        (SELECT COUNT(result) FROM nn_log WHERE result = -1) as 'Lost', 
        (SELECT COUNT(result) FROM nn_log WHERE result = -1)/COUNT(result)*100 as 'Lost Percentage', 
        (SELECT SUM(visited) FROM nn_neuron)/COUNT(result) as 'AVG Neurons per Game'
    FROM nn_log;
""")
scores = cursor.fetchone()

# The following query does almost exactly the same as the previous but 
# it groups the results into every 10,000 games. This allows for an
# overview of the learning as time goes on. 
cursor.execute("""
    SELECT 
        floor(id / 100) ym, 
        COUNT(result) as 'Total Games', 
        SUM(result) as 'Score', 
        (SELECT COUNT(result) FROM nn_log WHERE result = 1 and floor(id/100) = ym) as 'Won', 
        (SELECT COUNT(result) FROM nn_log WHERE result = 1 and floor(id/100) = ym)/COUNT(result)*100 as 'Won Percentage', 
        (SELECT COUNT(result) FROM nn_log WHERE result = 0 and floor(id/100) = ym) as 'Drawn', 
        (SELECT COUNT(result) FROM nn_log WHERE result = 0 and floor(id/100) = ym)/COUNT(result)*100 as 'Drawn Percentage', 
        (SELECT COUNT(result) FROM nn_log WHERE result = -1 and floor(id/100) = ym) as 'Lost', 
        (SELECT COUNT(result) FROM nn_log WHERE result = -1 and floor(id/100) = ym)/COUNT(result)*100 as 'Lost Percentage' 
    FROM nn_log 
    GROUP BY ym;
""")

#>>> print()

grouped = cursor.fetchall()

print "Total Neurons\t\t", locale.format("%d", totals[0], grouping=True)
print "Total Activations\t", locale.format("%d", totals[1], grouping=True)
print "AVG Neurons per Game\t", scores[8]

print "\n"

print "Games\t\tScore\t\tWon\tWon%\t\tDrawn\tDrawn%\t\tLost\tLost%"
print scores[0], "\t\t", scores[1], "\t\t", scores[2], "\t", 
print round(scores[3],2), "\t\t", scores[4], "\t", round(scores[5],2), 
print "\t\t", scores[6], "\t", round(scores[7],2)

print "\n"

print "Games\t\tScore\t\tWon\tWon%\t\tDrawn\tDrawn%\t\tLost\tLost%"
for group in grouped:
    print group[1], "\t\t", group[2], "\t\t", group[3], "\t", 
    print round(group[4],2), "\t\t", group[5], "\t", round(group[6],2), 
    print "\t\t", group[7], "\t", round(group[8],2)

print "\n"


import os
import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from pycala import GRAPH_STORE

won = [g[4] for g in grouped]
drawn = [g[6] for g in grouped]
lost = [g[8] for g in grouped]

fig = Figure()

for result in [won,drawn,lost,]:
    
    ax = fig.add_subplot(111)
    ax.set_xlabel('Games in thousands')
    ax.set_ylabel('Percentage')
    ax.set_title('Won Drawn Lost')
    x = []
    y = []
    y_c = 0
    for i in result:
        y.append(i)
        x.append(y_c)
        y_c += 1
    
    ax.set_xticks([i for i in xrange(len(x))], minor=False)
    
    l1 = ax.plot(x,y,'-', label='')
    
    ax.legend(loc='upper left')

canvas=FigureCanvas(fig)

filename = str(os.path.join(GRAPH_STORE, 'wdl', 'wdl %s %s.png'%(datetime.datetime.now().hour, datetime.datetime.now().minute),))

fig.savefig(filename, dpi=300) 
