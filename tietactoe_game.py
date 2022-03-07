""" Game File for OpenCV TicTacToe

File: tictactoe_game.py
Author: Jared Gregor
Date: 3/6/22

"""

import tictactoe

if __name__ == "__main__":
    print("\nWelcome to TicTacToe!")

    # Game Loop
    while(True):
        playerSelect = input("\nPress 'c' to play against the computer, 'u' to play two player, 'b' to exit: ")
        
        # Check user input
        if(playerSelect == 'b'):
            # Quit game
            print("Quitting game... Thanks for playing!\n")
            break

        elif(playerSelect == 'c'):
            # Play against computer
            tictactoe.TicTacToe(singlePlayer=True).play()

        elif(playerSelect == 'u'):
            # Play 2 player
            tictactoe.TicTacToe(singlePlayer=False).play()

        else:
            print("Invalid selection.")