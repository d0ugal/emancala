# Import all the test modules. This is a nasty hack, nose should do this
# for me, but doesn't for some unknown reason.

#from tests.cli. ?? import *

from tests.engine.board import *
from tests.engine.feature_detection import *
from tests.engine.players import *
from tests.engine.tournament import *

from tests.players.base import *
from tests.players.basic import *
from tests.players.evo import *
from tests.players.nn import *

from tests.runner.simple import *

#from tests.web. ?? import *