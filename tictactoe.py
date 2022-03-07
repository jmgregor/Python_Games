""" Implementation File for TicTacToe

File: tictactoe.py
Author: Jared Gregor
Date: 3/6/22

"""
import numpy as np
import cv2
import random

class TicTacToe:
    def __init__(self, singlePlayer):
        """ Initalize Game
        Create an empty game board and sets score to zero

        Args:
            singlePlayer (Boolean): Play against a CPU if True
        """
        # Set scores to zero
        self.score = [0, 0]

        # Set gameboard params
        self.squareSize = 200
        self.lineSize = 10
        
        # Create Empty gameboard
        self.gameboard = self.gameboard_clear()
        self.logicboard = np.zeros((3,3))
        self.moveCt = 0
        self.liveGame = True

        # Set to player 1's turn
        self.player1Turn = True

        # Set gametype to singleplayer
        self.singlePlayer = singlePlayer

    # Setters and Getters

    # Game Score
    def set_score(self, P1_score, P2_score):
        self.score = [P1_score, P2_score]
    def get_score(self):
        return self.score
    def print_score(self):
        score_P1, score_P2 = self.get_score()
        print("P1:", score_P1, "\tP2:", score_P2)

    # Square Size
    def set_squareSize(self, sideLength):
        self.set_squareSize = sideLength
    def get_squareSize(self):
        return self.squareSize

    # Line Size
    def set_lineSize(self, thickness):
        self.lineSize = thickness
    def get_lineSize(self):
        return self.lineSize

    # Game Methods

    def resetGame(self):
        self.gameboard = self.gameboard_clear()
        self.logicboard = np.zeros((3,3))
        self.moveCt = 0
        self.player1Turn = True
        self.liveGame = True

    def gameboard_clear(self):
        """ Clears gameboard
        Args: None
        Returns: Empty gameboard
        """
        # Define gameboard params
        SS, LS = self.squareSize, self.lineSize
        # Set empty board
        squares = np.ones((3*SS+2*LS, 3*SS+2*LS))
        # Draw lines
        for i in range(1,3):
            squares[SS*i + LS*(i-1):SS*i + LS*i, :] = 0
            squares[:, SS*i + LS*(i-1):SS*i + LS*i] = 0
        return squares

    def gameboard_update(self, square):
        """ Updates the gameboard to make a move on square
        Args:
            square (int, int)
        Returns: 
            None
        """
        # text point
        boxlen = self.gameboard.shape[0]//3 + 1
        offset = int(0.1 * self.get_squareSize())
        org = (square[1]*boxlen+offset, square[0]*boxlen+boxlen-offset)
        
        # Using cv2.putText() method
        player = "X" if self.player1Turn else "O"
        self.gameboard = cv2.putText(self.gameboard, player, org, cv2.FONT_HERSHEY_SIMPLEX, 8, 0, 10, cv2.LINE_AA)

        # Update logic board
        value = 1 if self.player1Turn else 2
        self.logicboard[square[0],square[1]] = value

        # Update move count
        self.moveCt += 1

    def play(self):
        """ Display Current gameboard """
        cv2.namedWindow("TicTacToe")
        cv2.setMouseCallback("TicTacToe", self.gameFunction)

        # keep looping until the 'q' key is pressed
        while True:
            # display the image and wait for a keypress
            cv2.imshow("TicTacToe", self.gameboard)
            key = cv2.waitKey(1) & 0xFF
            # if the 'r' key is pressed, reset the gameboard
            if key == ord("r"):
                self.resetGame()
            # if the 'q' key is pressed, break from the loop
            elif key == ord("q"):
                break

        # close all open windows
        cv2.destroyAllWindows()

    def end_message(self):
        w, h = self.gameboard.shape
        thickness = 4
        self.gameboard[w//8:w-w//8,h//8:h-h//8] = self.gameboard[w//8:w-w//8,h//8:h-h//8] - 0.8  # Grey box
        self.gameboard = cv2.putText(self.gameboard, "Game over", (h//8 + 15, w//8+(w-w//4)//2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.5, 1, thickness, cv2.LINE_AA)

        if(self.isWinner()):
            # Show who won
            player = 1 if self.player1Turn else 2
            self.gameboard = cv2.putText(self.gameboard, "Player " + str(player) + " wins!", (h//3, w//8+(w-w//4)//2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 1, 2, cv2.LINE_AA)
        else:
            # Out of turns
            self.gameboard = cv2.putText(self.gameboard, "Out of turns", (h//3, w//8+(w-w//4)//2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 1, 2, cv2.LINE_AA)

        # Display score
        P1_score, P2_score = self.get_score()
        self.gameboard = cv2.putText(self.gameboard, "P1: " + str(P1_score) + "   P2: " + str(P2_score) , (h//3, w//8+(w-w//4)//2 + 80), cv2.FONT_HERSHEY_SIMPLEX, 1, 1, 1, cv2.LINE_AA)

        # Show game options
        self.gameboard = cv2.putText(self.gameboard, "Press 'r' to replay or 'q' to quit", (h//8 + 40, w//8+(w-w//4)//2 + 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, 1, 1, cv2.LINE_AA)


    def gameFunction(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP and self.liveGame and self.isValidMove(self.coord2square((y,x))):
            for round in range(2 if self.singlePlayer else 1):
                # Player Selected coord
                if not self.singlePlayer or self.player1Turn:
                    squareID = self.coord2square((y,x))

                # CPU Selected coord    
                else:
                    validMove = False
                    while(not validMove):
                        squareID = (random.randint(0,2), random.randint(0,2))
                        validMove = self.isValidMove(squareID)

                # Make a move on selected point
                self.gameboard_update(squareID)

                # Check for win
                if(self.isWinner()):
                    # update score
                    self.score[0 if self.player1Turn else 1] += 1
                    # Show win message
                    self.end_message()
                    break
                # Check for out of turns
                elif (self.moveCt == 9):
                    self.end_message()
                    break
                # Next player
                else:
                    self.player1Turn = not self.player1Turn
    
    def isWinner(self):
        """ Checks if there is a win using game logic """
        player = 1 if self.player1Turn else 2
        win = False
        # Check rows and columns
        for i in range(3):
            if(np.all(self.logicboard[:,i] == player) or np.all(self.logicboard[i,:] == player)):
                win = True
        # Check diagonals
            if(np.all(np.diagonal(self.logicboard) == player) or np.all(np.flipud(self.logicboard).diagonal() == player)):
                win = True

        self.liveGame = not win
        return win

    def isValidMove(self, square):
        """ Checks if the selected point is a valid move
        Args:
            (x, y) (int, int) values from user or computer selection
        Returns:
            Boolean
        """
        boxlen = self.gameboard.shape[0]//3 + 1
        return np.sum(self.gameboard[square[0]*boxlen : square[0]*boxlen+boxlen , square[1]*boxlen : square[1]*boxlen+boxlen]) == self.get_squareSize()**2

    def coord2square(self, coordinate):
        """ Convert (row, col) coordinate to gameboard ROI
        Args:
            (int, int) coordinate as (row, col)
        Returns: ROI position in gameboard
        # __0_0__|__0_1__|__0_2__
        # __1_0__|__1_1__|__1_2__
        #   2 0  |  2 1  |  2 2  
        """
        row = coordinate[0] // (self.squareSize+(self.lineSize//2))
        col = coordinate[1] // (self.squareSize+(self.lineSize//2))
        return (row, col)


# --- Test Harness --- #
if __name__ == "__main__":
    """ Implementation of Player vs Computer TicTacToe """
    TicTacToe(singlePlayer=True).play()

    """ Implementation of Player vs Player TicTacToe """
    #TicTacToe(singlePlayer=False).play()