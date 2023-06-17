from __future__ import annotations

import re

from Board import Board
from Move import Move
from Pawn import Pawn


class InputParser:
    def __init__(self, board: Board, side: bool):
        self.board = board
        self.side = side

    def parse(self, humanInput: str) -> Move:
        regexCoordinateNotation = re.compile('(?i)[a-h][1-8][a-h][1-8][QRBN]?')
        if regexCoordinateNotation.match(humanInput):
            return self.moveForCoordinateNotation(humanInput)
        regexAlgebraicNotation = re.compile(
            '(?i)0-0|0-0-0|(?:[KQRBNP]?[a-h]?[1-8]?x?[a-h][1-8]|[Pa-h]x?[a-h])(?:=?[QRBN])?' 
        )
        if regexAlgebraicNotation.match(humanInput):
            return self.moveForShortAlgebraicNotation(humanInput)
        if re.compile('(?i)O-O|O-O-O').match(humanInput):
            return self.moveForShortAlgebraicNotation(
                humanInput.upper().replace('O', '0')
            )
        raise ValueError('Invalid move: %s' % humanInput)

    def moveForCoordinateNotation(self, notation: str) -> Move:
        for move in self.board.getAllMovesLegal(self.side):
            if self.board.getCoordinateNotationOfMove(
                    move).lower() == notation.lower():
                move.notation = self.notationForMove(move)
                return move
        raise ValueError('Illegal move: %s' % notation)
   
    def moveForShortAlgebraicNotation(self, notation: str) -> Move:
        shortNotation = notation.replace('x', '')
        moves = self.getLegalMovesWithNotation(self.side, False)
        for move in moves:
            if move.notation.replace('x', '') == shortNotation:
                return move 
        for move in moves:
            if move.notation.replace('x', '').lower() == shortNotation.lower():
                return move
        moves = self.getLegalMovesWithNotation(self.side, True)
        for move in moves:
            if move.notation.replace('x', '') == shortNotation:
                return move 
        for move in moves:
            if move.notation.replace('x', '').lower() == shortNotation.lower():
                return move
        shortNotation = notation.lower().replace('p', '').replace('=', '')
        if re.compile('[a-h][1-8]?[qrbn]?').match(shortNotation):
            for move in moves:
                if type(move.piece) is Pawn and not move.pieceToCapture \
                        and self.board.getCoordinateNotationOfMove(
                        move).replace('=', '').lower().endswith(shortNotation):
                    return move
            for move in moves:
                if type(move.piece) is Pawn and not move.pieceToCapture \
                        and re.sub(
                        '[1-8]', '', self.board.getCoordinateNotationOfMove(
                                move), ).replace('=', '').lower().endswith(
                        shortNotation):
                    return move 
        shortNotation = shortNotation.lower().replace('x', '')
        if re.compile('[a-h]?[a-h][1-8]?[qrbn]?').match(shortNotation):
            for move in moves:
                if type(move.piece) is Pawn and move.pieceToCapture \
                        and self.board.getCaptureNotation(
                        move).replace('x', '').lower().endswith(shortNotation):
                   
                    return move
            for move in moves:
                if type(move.piece) is Pawn and move.pieceToCapture and re.sub(
                        '[1-8]', '',
                        self.board.getCaptureNotation(move).replace('x',
                                                                    ''),
                ).lower().endswith(shortNotation):
                   
                    return move
        raise ValueError('Illegal move: %s' % notation)

    def notationForMove(self, move: Move) -> str:
        side = self.board.getSideOfMove(move)
        moves = self.getLegalMovesWithNotation(side)
        for m in moves:
            if m == move:
                return m.notation
        return '' 

    def getLegalMovesWithNotation(
            self, side: bool, short: bool = True) -> list[Move]:
        moves = []
        for legalMove in self.board.getAllMovesLegal(side):
            moves.append(legalMove)
            legalMove.notation = self.board.getAlgebraicNotationOfMove(
                legalMove, short
            )

        duplicateNotationMoves = self.duplicateMovesFromMoves(moves)
        for duplicateMove in duplicateNotationMoves:
            duplicateMove.notation = self.board.getAlgebraicNotationOfMoveWithFile( 
                duplicateMove, short
            )

        duplicateNotationMoves = self.duplicateMovesFromMoves(moves)
        for duplicateMove in duplicateNotationMoves:
            duplicateMove.notation = self.board.getAlgebraicNotationOfMoveWithRank( 
                duplicateMove, short
            )

        duplicateNotationMoves = self.duplicateMovesFromMoves(moves)
        for duplicateMove in duplicateNotationMoves:
            duplicateMove.notation = self.board.getAlgebraicNotationOfMoveWithFileAndRank( 
                duplicateMove, short
            )

        return moves

    def duplicateMovesFromMoves(self, moves: list[Move]) -> list[Move]:
        return list(
            filter(
                lambda move: len(
                    [m for m in moves if m.notation == move.notation]
                )
                > 1,
                moves,
            )
        )