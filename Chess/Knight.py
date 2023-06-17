from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from Coordinate import Coordinate as C
from Move import Move
from Piece import Piece

if TYPE_CHECKING:
    from Board import Board

WHITE = True
BLACK = False


class Knight(Piece):
    stringRep = 'N'
    value = 3

    def __init__(
            self, board: Board, side: bool, position: C, movesMade: int = 0
    ) -> None:
        super(Knight, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self) -> Iterator[Move]:
        board = self.board
        currentPos = self.position
        movements = [
            C(2, 1),
            C(2, -1),
            C(-2, 1),
            C(-2, -1),
            C(1, 2),
            C(1, -2),
            C(-1, -2),
            C(-1, 2),
        ]
        for movement in movements:
            newPos = currentPos + movement
            if board.isValidPos(newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)
