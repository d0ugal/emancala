# The engine package contains the functionality for controling the game
# and enforcing rules. It includes the functionality to run multiple 
# games and simple round-robin tournament based runs.

"""
A board shown below with the pit numbers and how they are referenced.
The numbers represent the position in a list.
                   PLAYER B (FALSE)
.----------------------------------------------.
| .----. .--. .--. .--. .--. .--. .--. .----.  |
| |    | |12| |11| |10| | 9| | 8| | 7| |    |  |
| | 13 | '--' '--' '--' '--' '--' '--' | 6  |  |
| |    | .--. .--. .--. .--. .--. .--. |    |  |
| |    | | 0| | 1| | 2| | 3| | 4| | 5| |    |  |
| '----' '--' '--' '--' '--' '--' '--' '----'  |
'----------------------------------------------'
                    PLAYER A (TRUE)
"""

"""
Various game states
"""
GAME_STARTED    = 0 # Uninitialised game
GAME_RUNNING    = 1 # Game thats underway
GAME_FINISHED   = 2 # Game thats finished

GAME_UNKNOWN = 0 # Unfinished Game
GAME_WON_A   = 1 # Finished game, won by PLAYER_A
GAME_WON_B   = 2 # Finished game, won by PLAYER_B
GAME_DRAW    = 3 # Finished game, draw

"""
Players turn as a boolean for convenience as after each turn you
can then do "players_turn = not players_turn" to flip it
"""
PLAYER_A = True
PLAYER_B = not PLAYER_A

"""
The home pits for both players for convenience
"""
HOME_A = 6
HOME_B = 13

"""
Array of playable pits for each player
"""
PITS_A = range(0,HOME_A) # 0 - 5
PITS_B = range(7,HOME_B) # 7 - 12

"""
Valid start board, this is only used for testing purposes.
"""
VALID_START_BOARD = [4,4,4,4,4,4,0,4,4,4,4,4,4,0]