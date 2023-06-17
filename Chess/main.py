from __future__ import annotations
import random

from Bot import Bot
from Board import Board
from InputParser import InputParser
from Move import Move

WHITE = True
BLACK = False


def printCommandOptions() -> None:
    printLegalMovesOption = 'l : show all legal moves'
    randomMoveOption = 'r : make a random move'
    quitOption = 'quit : resign'
    moveOption = 'Make moves in Algebraic notation: i.e d6'
    options = [
        printLegalMovesOption,
        randomMoveOption,
        quitOption,
        moveOption,
        '',
    ]
    print('\n'.join(options))


def printAllLegalMoves(board: Board, parser: InputParser) -> None:
    for move in parser.getLegalMovesWithNotation(
        board.currentSide, short=True
    ):
        print(move.notation)


def getRandomMove(board: Board, parser: InputParser) -> Move:
    legalMoves = board.getAllMovesLegal(board.currentSide)
    randomMove = random.choice(legalMoves)
    randomMove.notation = parser.notationForMove(randomMove)
    return randomMove


def makeMove(move: Move, board: Board) -> None:
    print('Making move : ' + move.notation)
    board.makeMove(move)


def printBoard(board: Board) -> None:
    print()
    print(board)
    print()


def startGame(board: Board, playerSide: bool, bot: Bot) -> None:
    parser = InputParser(board, playerSide)
    while True:
        if board.isCheckmate():
            if board.currentSide == playerSide:
                print('Checkmate, you lost')
            else:
                print('Checkmate! You won!')
            return

        if board.isStalemate():
            print('Stalemate')
            return

        if board.noMatingMaterial():
            print('Draw')
            return

        if board.currentSide == playerSide:
            move = None
            command = input("'?' for options. ")
            if command.lower() == '?':
                printCommandOptions()
                continue
            elif command.lower() == 'l':
                printAllLegalMoves(board, parser)
                continue
            elif command.lower() == 'r':
                move = getRandomMove(board, parser)
            elif command.lower() == 'exit' or command.lower() == 'quit':
                return
            try:
                if move is None:
                    move = parser.parse(command)
            except ValueError as error:
                print('%s' % error)
                continue
            makeMove(move, board)
            printBoard(board)

        else:
            print('Calculating bot moves...')
            move = bot.getBestMove()
            move.notation = parser.notationForMove(move)
            makeMove(move, board)
            printBoard(board)

board = Board()


def main() -> None:
    board.isCheckered = False
    try:
        board.currentSide = WHITE
        print()
        opponentAI = Bot(board, BLACK, 2)
        printBoard(board)
        startGame(board, WHITE, opponentAI)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
