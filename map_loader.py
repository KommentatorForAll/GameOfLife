import cv2 as cv
import numpy as np
import main as gol

def main():
    img = cv.imread("test.png")
    game_board = np.array([[all(i == (255,255,255)) for i in x] for x in img])
    gol.size = (len(game_board[0]), len(game_board))
    gol.game_board = game_board
    gol.nb_grid = np.zeros(gol.size)
    gol.init()


if (__name__ == "__main__"):
    main()