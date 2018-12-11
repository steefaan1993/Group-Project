from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter

from piece import Piece


class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    # todo set the board with and height in square
    boardWidth = 8
    boardHeight = 8
    Speed = 300
    timerSpeed = 1000  # the timer updates ever 1 second
    counter = 10  # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()
        self.oldcol = 0
        self.oldrow = 0

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False
        self.start()

        # self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.resetGame()

        self.boardArray = [
            [8, 1, 8, 1, 8, 1, 8, 1],
            [1, 8, 1, 8, 1, 8, 1, 8],
            [8, 1, 8, 1, 8, 1, 8, 1],
            [0, 8, 0, 8, 0, 8, 0, 8],
            [8, 0, 8, 0, 8, 1, 8, 0],
            [2, 8, 2, 8, 2, 8, 2, 8],
            [8, 2, 8, 2, 8, 2, 8, 2],
            [2, 8, 2, 8, 2, 8, 2, 8]]  # 2d int/Piece array to story the state of the game
        self.possMov = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]
        self.printBoardArray()

    def resetPossMoves(self):
        self.possMov = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]

    def printBoardArray(self):
        '''prints the boardArray in an arractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def printPossArray(self):
        '''prints the boardArray in an arractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.possMov]))

    def mousePosToColRow(self, event):
        xMouseEvent = event.x()
        yMouseEvent = event.y()
        squareHeight = self.squareHeight()
        squareWidth = self.squareWidth()
        row = int(yMouseEvent / squareHeight)
        col = int(xMouseEvent / squareWidth)
        return row, col
        '''convert the mouse click event to a row and column'''

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / Board.boardWidth

    def squareHeight(self):
        '''returns the height of one squarein the board'''
        return self.contentsRect().height() / Board.boardHeight

    def start(self):
        '''starts game'''
        #if self.isPaused:
          #  return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.resetGame()

        self.msg2Statusbar.emit(str("status message"))

        self.timer.start(Board.Speed, self)

    def pause(self):
        '''pauses game'''

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")

        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str("status message"))
        self.update()

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPossibleMoves(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        print("click location [", event.x(), ",", event.y(), "]")
        # todo you could call some game locig here

        val = self.mousePosToColRow(event)
        print(val[0], val[1])

        if (self.boardArray[val[0]][val[1]] == 1):
            self.resetPossMoves()
            print('Yellow Piece is seleced')
            possmov = self.findingValidFieldsPlayer1(val[0], val[1])
            # print(possmov)
        if (self.boardArray[self.oldrow][self.oldcol] == 1):
            if (self.possMov[val[0]][val[1]] == 1):
                self.boardArray[self.oldrow][self.oldcol] = 0
                self.boardArray[val[0]][val[1]] = 1
                self.resetPossMoves()

        if (self.boardArray[val[0]][val[1]] == 2):
            self.resetPossMoves()
            print('Red Piece is seleced')
            possmov = self.findingValidFieldsPlayer2(val[0], val[1])
            # print(possmov)
        if (self.boardArray[self.oldrow][self.oldcol] == 2):
            if (self.possMov[val[0]][val[1]] == 1):
                self.boardArray[self.oldrow][self.oldcol] = 0
                self.boardArray[val[0]][val[1]] = 2
                self.resetPossMoves()

        self.oldrow = val[0]
        self.oldcol = val[1]

        # self.printBoardArray()
        self.printPossArray()

        self.update()

    # not yet tested
    def findingValidFieldsPlayer1(self, oldrow, oldcol):
        oldrow += 1
        if (oldrow < 8):
            if (self.boardArray[oldrow][oldcol - 1] == 0 and oldcol >= 0):
                self.possMov[oldrow][oldcol - 1] = 1
            elif (self.boardArray[oldrow][oldcol - 1] == 2 and oldcol >= 0):
                newrow = oldrow + 1
                oldcol -= 1
                if (newrow <= 7):
                    if (self.boardArray[oldrow][oldcol] == 0 and oldcol >= 0):
                        self.possMov[newrow][oldcol] = 1
            oldcol += 1
            if (oldcol <= 7):
                if (self.boardArray[oldrow][oldcol] == 0):
                    self.possMov[oldrow][oldcol] = 1
                elif (self.boardArray[oldrow][oldcol] == 2):
                    newrow = oldrow + 1
                    oldcol += 1
                    if (newrow <= 7):
                        if (self.boardArray[newrow][oldcol] == 0):
                            self.possMov[newrow][oldcol] = 1
                        elif (self.boardArray[newrow][oldcol - 2] == 0):
                            self.possMov[newrow][oldcol] = 1

        return self.possMov

    # not yet tested
    def findingValidFieldsPlayer2(self, oldrow, oldcol):
        oldrow -= 1
        if (oldrow < 8):
            if (self.boardArray[oldrow][oldcol - 1] == 0 and oldcol >= 0):
                if (oldcol - 1 >= 0):
                    self.possMov[oldrow][oldcol - 1] = 1

            elif (self.boardArray[oldrow][oldcol - 1] == 1 and oldcol >= 0):
                newrow = oldrow - 1
                newcol = oldcol - 1
                if (newrow <= 7):
                    if (self.boardArray[oldrow][newcol] == 0):
                        self.possMov[newrow][newcol] = 1

            if (oldcol <= 7):
                if (self.boardArray[oldrow][oldcol+1] == 0):
                    self.possMov[oldrow][oldcol+1] = 1

                elif (self.boardArray[oldrow][oldcol+1] == 1):
                    newrow = oldrow - 1
                    oldcol += 2
                    if (newrow <= 7):
                        if(oldcol<=7):
                            if (self.boardArray[newrow][oldcol] == 0):
                                self.possMov[newrow][oldcol] = 1
                            elif (self.boardArray[newrow][oldcol - 2] == 0):
                                self.possMov[newrow][oldcol] = 1

        return self.possMov

    def keyPressEvent(self, event):
        '''processes key press events if you would like to do any'''
        if not self.isStarted or self.curPiece.shape() == Piece.NoPiece:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)

        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)

        elif key == Qt.Key_Space:
            self.dropDown()

        elif key == Qt.Key_D:
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)

    def timerEvent(self, event):
        '''handles timer event'''
        # todo adapter this code to handle your timers

        # todo adapter this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            Board.counter = Board.counter - 1
            print('timerEvent()', Board.counter)
            self.updateTimerSignal.emit(Board.counter)
        else:
            super(Board, self).timerEvent(event)  # other wise pass it to the super class for handling

    def resetGame(self):
        '''clears pieces from the board'''
        # todo write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # todo set the dafault colour of the brush
        painter.setBrush(Qt.white)

        colTransformation = self.squareWidth()
        rowTransformation = self.squareHeight()
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                if ((row + col) % 2 == 0):
                    painter.setBrush(Qt.white)
                else:
                    painter.setBrush(Qt.black)

                rowprint = self.squareWidth()
                colprint = self.squareHeight()
                painter.save()
                painter.translate(col * colTransformation, row * rowTransformation)
                painter.fillRect(0, 0, rowprint, colprint, painter.brush())

                painter.restore()

    def drawPossibleMoves(self, painter):
        painter.setBrush(Qt.transparent)

        colTransformation = self.squareWidth()
        rowTransformation = self.squareHeight()
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                if (self.possMov[row][col] == 1):
                    painter.setBrush(Qt.cyan)
                rowprint = self.squareWidth()
                colprint = self.squareHeight()
                painter.save()
                painter.translate(col * colTransformation, row * rowTransformation)
                painter.fillRect(0, 0, rowprint, colprint, painter.brush())

                painter.restore()
                painter.setBrush(Qt.transparent)

    def drawPieces(self, painter):
        '''draw the prices on the board'''
        painter.setPen(Qt.transparent)
        painter.setBrush(Qt.transparent)
        colTransformation = self.squareWidth()
        rowTransformation = self.squareHeight()
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(col * colTransformation, row * rowTransformation)
                draw = False
                # Todo choose your colour and set the painter brush to the correct colour
                if self.boardArray[row][col] == 1:
                    painter.setBrush(Qt.yellow)

                elif self.boardArray[row][col] == 2:
                    painter.setBrush(Qt.red)

                # Todo draw some the pieces as elipses
                radiusW = (self.squareWidth() - 2) / 2
                radiusH = (self.squareHeight() - 2) / 2
                center = QPoint(radiusW, radiusH)
                painter.drawEllipse(center, radiusW, radiusH)
                painter.restore()
