from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from Bishop import Bishop
from Coordinate import Coordinate as C
from Knight import Knight
from Move import Move
from Piece import Piece
from Queen import Queen
from Rook import Rook

if TYPE_CHECKING:
    from Board import Board

WHITE = True
BLACK = False


class Pawn(Piece):
    stringRep = '▲'
    value = 1

    def __init__(
            self, board: Board, side: bool, position: C, movesMade: int = 0
    ) -> None:
        super(Pawn, self).__init__(board, side, position)
        self.movesMade = movesMade

   
    def getPossibleMoves(self) -> Iterator[Move]:
        currentPosition = self.position

       
        movement = C(0, 1) if self.side == WHITE else C(0, -1)
        advanceOnePosition = currentPosition + movement
        if self.board.isValidPos(advanceOnePosition):
           
            if self.board.pieceAtPosition(advanceOnePosition) is None:
                col = advanceOnePosition[1]
                if col == 7 or col == 0:
                    piecesForPromotion = [
                        Rook(self.board, self.side, advanceOnePosition),
                        Knight(self.board, self.side, advanceOnePosition),
                        Bishop(self.board, self.side, advanceOnePosition),
                        Queen(self.board, self.side, advanceOnePosition),
                    ]
                    for piece in piecesForPromotion:
                        move = Move(self, advanceOnePosition)
                        move.promotion = True
                        move.specialMovePiece = piece 
                        yield move
                else:
                    yield Move(self, advanceOnePosition)

       
        if self.movesMade == 0:
            movement = C(0, 2) if self.side == WHITE else C(0, -2)
            advanceTwoPosition = currentPosition + movement
            if self.board.isValidPos(advanceTwoPosition):
                if (
                        self.board.pieceAtPosition(advanceTwoPosition) is None
                        and self.board.pieceAtPosition(
                            advanceOnePosition) is None
                ):
                    yield Move(self, advanceTwoPosition)

       
        movements = (
            [C(1, 1), C(-1, 1)]
            if self.side == WHITE
            else [C(1, -1), C(-1, -1)]
        )

        for movement in movements:
            newPosition = self.position + movement
            if self.board.isValidPos(newPosition):
                pieceToTake = self.board.pieceAtPosition(newPosition)
                if pieceToTake and pieceToTake.side != self.side:
                    col = newPosition[1]
                   
                    if col == 7 or col == 0:
                        piecesForPromotion = [
                            Rook(self.board, self.side, newPosition),
                            Knight(self.board, self.side, newPosition),
                            Bishop(self.board, self.side, newPosition),
                            Queen(self.board, self.side, newPosition),
                        ]
                        for piece in piecesForPromotion:
                            move = Move(
                                self, newPosition, pieceToCapture=pieceToTake
                            )
                            move.promotion = True
                            move.specialMovePiece = piece 
                            yield move
                    else:
                        yield Move(
                            self, newPosition, pieceToCapture=pieceToTake
                        )

       
        movements = (
            [C(1, 1), C(-1, 1)]
            if self.side == WHITE
            else [C(1, -1), C(-1, -1)]
        )
        for movement in movements:
            posBesidePawn = self.position + C(movement[0], 0)
            if not self.board.isValidPos(posBesidePawn):
                continue
            pieceBesidePawn = self.board.pieceAtPosition(posBesidePawn)
            lastPieceMoved = self.board.getLastPieceMoved()
            lastMoveWasAdvanceTwo = False
            lastMove = self.board.getLastMove()

            if lastMove:
                if (
                        lastMove.newPos - lastMove.oldPos == C(0, 2)
                        or lastMove.newPos - lastMove.oldPos == C(0, -2)
                ):
                    lastMoveWasAdvanceTwo = True

            if (
                    pieceBesidePawn
                    and pieceBesidePawn.stringRep == Pawn.stringRep
                    and pieceBesidePawn.side != self.side
                    and lastPieceMoved is pieceBesidePawn
                    and lastMoveWasAdvanceTwo
            ):
                move = Move(
                    self,
                    self.position + movement,
                    pieceToCapture=pieceBesidePawn,
                )
                move.passant = True
                move.specialMovePiece = pieceBesidePawn 
                yield move
