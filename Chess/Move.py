from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Coordinate import Coordinate as C
    from Piece import Piece


class Move:
    def __init__(
            self,
            piece: Piece,
            newPos: C,
            pieceToCapture: Optional[Piece] = None
    ) -> None:
        self.notation = ''
        self.checkmate = False
        self.kingsideCastle = False
        self.queensideCastle = False
        self.promotion = False
        self.passant = False
        self.stalemate = False

        self.piece = piece
        self.oldPos = piece.position
        self.newPos = newPos
        self.pieceToCapture = pieceToCapture
        self.specialMovePiece = None
        self.rookMove = None

    def __str__(self) -> str:
        displayString = 'Old pos : ' + str(self.oldPos) + \
                        ' -- New pos : ' + str(self.newPos)
        if self.notation:
            displayString += ' Notation : ' + self.notation
        if self.passant:
            displayString = 'Old pos : ' + str(self.oldPos) + \
                            ' -- New pos : ' + str(self.newPos) + \
                            ' -- Pawn taken : ' + str(self.specialMovePiece)
            displayString += ' PASSANT'
        return displayString

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            return NotImplemented
        if (
                self.oldPos == other.oldPos and self.newPos == other.newPos
                and self.specialMovePiece == other.specialMovePiece
        ):
            if not self.specialMovePiece:
                return True
            if (
                    self.specialMovePiece
                    and self.specialMovePiece == other.specialMovePiece
            ):
                return True
            else:
                return False
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.oldPos, self.newPos))
