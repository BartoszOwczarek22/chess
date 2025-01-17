from __future__ import annotations

import random

from Board import Board
from InputParser import InputParser
from Move import Move
from MoveNode import MoveNode

WHITE = True
BLACK = False


class Bot:
    depth = 1
    movesAnalyzed = 0

    def __init__(self, board: Board, side: bool, depth: int):
        self.board = board
        self.side = side
        self.depth = depth
        self.parser = InputParser(self.board, self.side)

    def getRandomMove(self) -> Move:
        legalMoves = list(self.board.getAllMovesLegal(self.side))
        randomMove = random.choice(legalMoves)
        return randomMove

    def generateMoveTree(self) -> list[MoveNode]:
        moveTree = []
        for move in self.board.getAllMovesLegal(self.side):
            moveTree.append(MoveNode(move, [], None))

        for node in moveTree:
            self.board.makeMove(node.move)
            self.populateNodeChildren(node)
            self.board.undoLastMove()
        return moveTree

    def populateNodeChildren(self, node: MoveNode) -> None:
        node.pointAdvantage = self.board.getPointAdvantageOfSide(self.side)
        node.depth = node.getDepth()
        if node.depth == self.depth:
            return

        side = self.board.currentSide

        legalMoves = self.board.getAllMovesLegal(side)
        if not legalMoves:
            if self.board.isCheckmate():
                node.move.checkmate = True
                return
            elif self.board.isStalemate():
                node.move.stalemate = True
                node.pointAdvantage = 0
                return
            raise Exception()

        for move in legalMoves:
            self.movesAnalyzed += 1
            node.children.append(MoveNode(move, [], node))
            self.board.makeMove(move)
            self.populateNodeChildren(node.children[-1])
            self.board.undoLastMove()

    def getOptimalPointAdvantageForNode(self, node: MoveNode) -> int:
        if node.children:
            for child in node.children:
                child.pointAdvantage = self.getOptimalPointAdvantageForNode(
                    child
                )

            if node.children[0].depth % 2 == 1:
                return max(node.children).pointAdvantage
            else:
                return min(node.children).pointAdvantage
        else:
            return node.pointAdvantage

    def getBestMove(self) -> Move:
        if self.board.getPointValueOfSide(WHITE) <= 105:
            self.depth = 8
        moveTree = self.generateMoveTree()
        bestMoves = self.bestMovesWithMoveTree(moveTree)
        randomBestMove = random.choice(bestMoves)
        randomBestMove.notation = self.parser.notationForMove(randomBestMove)
        return randomBestMove

    def makeBestMove(self) -> None:
        self.board.makeMove(self.getBestMove())

    def bestMovesWithMoveTree(self, moveTree: list[MoveNode]) -> list[Move]:
        bestMoveNodes: list[MoveNode] = []
        for moveNode in moveTree:
            moveNode.pointAdvantage = self.getOptimalPointAdvantageForNode(
                moveNode
            )
            if not bestMoveNodes:
                bestMoveNodes.append(moveNode)
            elif moveNode > bestMoveNodes[0]:
                bestMoveNodes = []
                bestMoveNodes.append(moveNode)
            elif moveNode == bestMoveNodes[0]:
                bestMoveNodes.append(moveNode)

        return [node.move for node in bestMoveNodes]


if __name__ == '__main__':
    mainBoard = Board()
    bot = Bot(mainBoard, True, 8)
    print(mainBoard)
    bot.makeBestMove()
    print(mainBoard)
    print(bot.movesAnalyzed)
    print(mainBoard.movesMade)
