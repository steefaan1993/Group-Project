from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor

from piece import Piece


class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location

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
        '''initiates board with timer and the board array which
        is the basic for the drawing of the board and the pieces
        0 are all empty fields on board. 1s are the pieces for the first player.
        2s are the pieces for player2. 8s are all the white squaeres on the field'''
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False
        self.start()


        self.isStarted = False
        self.isPaused = False
        self.resetGame()
        self.jumpp1=0
        self.jumpp2=0

        self.ColorP1 = Qt.yellow
        self.ColorP2 = Qt.red

        self.P1Turn=True

        self.boardArray = [
            [8, 4, 8, 1, 8, 1, 8, 1],
            [1, 8, 1, 8, 1, 8, 1, 8],
            [8, 1, 8, 2, 8, 1, 8, 1],
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

    def resetBoardArray(self):
        '''Method for reseting the board array to its initial state'''
        self.boardArray = [
            [8, 4, 8, 1, 8, 1, 8, 1],
            [1, 8, 1, 8, 1, 8, 1, 8],
            [8, 1, 8, 2, 8, 1, 8, 1],
            [0, 8, 0, 8, 0, 8, 0, 8],
            [8, 0, 8, 0, 8, 1, 8, 0],
            [2, 8, 2, 8, 2, 8, 2, 8],
            [8, 2, 8, 2, 8, 2, 8, 2],
            [2, 8, 2, 8, 2, 8, 2, 8]]


    def resetPossMoves(self):
        '''Method for resetting the possible move array'''
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
        '''prints the Possible MoveArray in an arractive way'''
        print("PossMocdArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.possMov]))

    def mousePosToColRow(self, event):
        '''Method for translate mouseposition to the row and the colum of the board'''
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
        '''paints the board, the pieces of the game
        and the possible moves a player can make'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPossibleMoves(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''Method for handling the event of the mouse pressing,
        this means that when someones clicks on a piece it gets selected
         and when the user selectes a square which is highlighted the piece moves to this position.
         At first it checks what kind of a piece and from what player it is.
         Then it calls the methods for finding the possible moves for that piece.
         After that it checks if a caputre is happening and incremnts the capture counter.
         After that it checks if there is a piece which needs to be turnend into a king.'''
        print("click location [", event.x(), ",", event.y(), "]")


        val = self.mousePosToColRow(event)
        print(val[0], val[1])

        if(self.P1Turn==True):

            if (self.boardArray[val[0]][val[1]] == 1):
                self.resetPossMoves()
                print('Yellow Piece is seleced')
                self.possMov = self.findingValidFieldsPlayer1(val[0], val[1])


            elif(self.boardArray[val[0]][val[1]] ==3):
                self.resetPossMoves()
                print('Yellow King is seleced')
                self.possMov = self.findingValidMovesForKing(val[0], val[1])


            if (self.boardArray[self.oldrow][self.oldcol] == 3):
                if (self.possMov[val[0]][val[1]] == 1):
                    if(self.oldcol+2==val[1]):
                        self.boardArray[self.oldrow+1][self.oldcol+1]=0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 3
                        self.jumpp1+=1
                        self.resetPossMoves()
                    elif (self.oldcol - 2 == val[1]):
                        self.boardArray[self.oldrow + 1][self.oldcol - 1] = 0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 3
                        self.jumpp1 += 1
                        self.resetPossMoves()
                    elif (self.oldcol + 2 == val[1]):
                        self.boardArray[self.oldrow - 1][self.oldcol + 1] = 0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 3
                        self.jumpp1 += 1
                        self.resetPossMoves()
                    elif (self.oldcol - 2 == val[1]):
                        self.boardArray[self.oldrow - 1][self.oldcol - 1] = 0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 3
                        self.jumpp1 += 1
                        self.resetPossMoves()
                    else:
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 3
                        self.resetPossMoves()
                        self.P1Turn = False

            if (self.boardArray[self.oldrow][self.oldcol] == 1):
                if (self.possMov[val[0]][val[1]] == 1):
                    if(self.oldcol+2==val[1]):
                        self.boardArray[self.oldrow+1][self.oldcol+1]=0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 1
                        if (val[0] == 7):
                            self.boardArray[val[0]][val[1]] = 3
                        self.jumpp1+=1
                        self.resetPossMoves()
                    elif (self.oldcol - 2 == val[1]):
                        self.boardArray[self.oldrow + 1][self.oldcol - 1] = 0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 1
                        if (val[0] == 7):
                            self.boardArray[val[0]][val[1]] = 3
                        self.jumpp1 += 1
                        self.resetPossMoves()
                    else:
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 1
                        if (val[0] == 7):
                            self.boardArray[val[0]][val[1]] = 3
                        self.resetPossMoves()
                        self.P1Turn=False

        if(self.P1Turn==False):

            if (self.boardArray[val[0]][val[1]] == 2):
                self.resetPossMoves()
                print('Red Piece is seleced')
                self.possMov = self.findingValidFieldsPlayer2(val[0], val[1])
                # print(possmov)
            elif (self.boardArray[val[0]][val[1]] == 4):
                self.resetPossMoves()
                print('Red King is seleced')
                self.possMov = self.findingValidMovesForKing(val[0], val[1])
                # print(possmov)
            if (self.boardArray[self.oldrow][self.oldcol] == 4):
                if (self.possMov[val[0]][val[1]] == 1):
                    if(self.oldcol+2==val[1]):
                        self.boardArray[self.oldrow+1][self.oldcol+1]=0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 4
                        self.jumpp2+=1
                        self.resetPossMoves()
                    elif (self.oldcol - 2 == val[1]):
                        self.boardArray[self.oldrow + 1][self.oldcol - 1] = 0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 4
                        self.jumpp2 += 1
                        self.resetPossMoves()
                    elif (self.oldcol + 2 == val[1]):
                        self.boardArray[self.oldrow - 1][self.oldcol + 1] = 0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 4
                        self.jumpp2 += 1
                        self.resetPossMoves()
                    elif (self.oldcol - 2 == val[1]):
                        self.boardArray[self.oldrow - 1][self.oldcol - 1] = 0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 4
                        self.jumpp2 += 1
                        self.resetPossMoves()
                    else:
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 4
                        self.resetPossMoves()
                        self.P1Turn=True

            if (self.boardArray[self.oldrow][self.oldcol] == 2):
                if (self.possMov[val[0]][val[1]] == 1):
                    if (self.oldcol + 2 == val[1]):
                        self.boardArray[self.oldrow - 1][self.oldcol + 1] = 0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 2
                        if(val[0]==0):
                            self.boardArray[val[0]][val[1]] = 4
                        self.jumpp2 += 1
                        self.resetPossMoves()
                    elif (self.oldcol - 2 == val[1]):
                        self.boardArray[self.oldrow - 1][self.oldcol - 1] = 0
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 2
                        if (val[0] == 0):
                            self.boardArray[val[0]][val[1]] = 4
                        self.jumpp2 += 1
                        self.resetPossMoves()
                    else:
                        self.boardArray[self.oldrow][self.oldcol] = 0
                        self.boardArray[val[0]][val[1]] = 2
                        if (val[0] == 0):
                            self.boardArray[val[0]][val[1]] = 4
                        self.resetPossMoves()
                        self.P1Turn=True

        self.oldrow = val[0]
        self.oldcol = val[1]


        self.printPossArray()

        self.update()

    def findingValidMovesForKing(self, oldrow, oldcol):
        '''Method for finding the possible squares to move to for a king for both players.
        At first it checks for vvalid fields in the row above.
        If there is a piece of a opposite player on a valid field it checks for valid fields in the row above.
        Then it checks in the row below the starting row for valid fields.
        If there is a piece of a opposite player on a valid field it checks the row below for valid fields.'''
        jumpPossible = False
        oldrow += 1
        if (oldrow < 8):
            if (self.boardArray[oldrow][oldcol - 1] == 0 and oldcol - 1 >= 0):
                if (oldcol - 1 >= 0):
                    self.possMov[oldrow][oldcol - 1] = 1
            if (self.boardArray[oldrow][oldcol - 1] == 2 and oldcol - 1 >= 0):
                newrow = oldrow + 1
                newcol = oldcol - 2
                if (newrow <= 7):
                    if (newcol >= 0):
                        if (self.boardArray[newrow][newcol] == 0 and oldcol >= 0):
                            self.resetPossMoves()
                            jumpPossible = True
                            self.possMov[newrow][newcol] = 1

            if (oldcol + 1 <= 7 and jumpPossible == False):
                if (self.boardArray[oldrow][oldcol + 1] == 0):
                    self.possMov[oldrow][oldcol + 1] = 1

                elif (self.boardArray[oldrow][oldcol + 1] == 2):
                    newrow = oldrow + 1
                    newcol = oldcol + 2
                    if (newrow <= 7 and newrow >= 0):
                        if (newcol <= 7):
                            if (self.boardArray[newrow][newcol] == 0 and jumpPossible == False):
                                self.resetPossMoves()
                                self.possMov[newrow][newcol] = 1

            oldrow -= 2
            if (oldrow <= 7 and oldrow >= 0):
                if (self.boardArray[oldrow][oldcol - 1] == 0):
                    if (oldcol - 1 >= 0):
                        self.possMov[oldrow][oldcol - 1] = 1

                if (self.boardArray[oldrow][oldcol - 1] == 1):
                    newrow = oldrow - 1
                    newcol = oldcol - 2
                    if (newrow <= 7 and newrow >= 0):
                        if (self.boardArray[newrow][newcol] == 0):
                            self.resetPossMoves()
                            jumpPossible = True
                            self.possMov[newrow][newcol] = 1

                if (oldcol + 1 <= 7 and jumpPossible == False):
                    if (self.boardArray[oldrow][oldcol + 1] == 0):
                        self.possMov[oldrow][oldcol + 1] = 1

                    elif (self.boardArray[oldrow][oldcol + 1] == 1):
                        newrow = oldrow - 1
                        newcol = oldcol + 2
                        if (newrow <= 7 and newrow >= 0):
                            if (oldcol <= 7):
                                if (self.boardArray[newrow][newcol] == 0 and jumpPossible == False):
                                    self.resetPossMoves()
                                    self.possMov[newrow][newcol] = 1

        return self.possMov


    def findingValidFieldsPlayer1(self, oldrow, oldcol):
        '''Method for finding the possible squares to move to for a piece of player1.
        At first it checks for vvalid fields in the row above.
        If there is a piece of a opposite player on a valid field it checks for valid fields in the row above.'''
        jumpPossible = False
        oldrow += 1
        if (oldrow < 8):
            if (self.boardArray[oldrow][oldcol - 1] == 0 and oldcol-1 >= 0):
                if(oldcol-1>=0):
                    self.possMov[oldrow][oldcol - 1] = 1
            if (self.boardArray[oldrow][oldcol - 1] == 2 and oldcol-1 >= 0):
                newrow = oldrow + 1
                newcol = oldcol - 2
                if (newrow <= 7):
                    if(newcol>=0):
                        if (self.boardArray[newrow][newcol] == 0 and oldcol >= 0):
                            self.resetPossMoves()
                            jumpPossible = True
                            self.possMov[newrow][newcol] = 1

            if (oldcol + 1 <= 7 and jumpPossible == False):
                if (self.boardArray[oldrow][oldcol + 1] == 0):
                    self.possMov[oldrow][oldcol + 1] = 1

                elif (self.boardArray[oldrow][oldcol + 1] == 2):
                    newrow = oldrow + 1
                    newcol=oldcol + 2
                    if (newrow <= 7 and newrow >= 0):
                        if (newcol <= 7):
                            if (self.boardArray[newrow][newcol] == 0 and jumpPossible == False):
                                self.resetPossMoves()
                                self.possMov[newrow][newcol] = 1


        return self.possMov


    def findingValidFieldsPlayer2(self, oldrow, oldcol):
        '''Method for finding the possible squares to move to for a piece of player2.
                At first it checks for vvalid fields in the row below the starting row.
                If there is a piece of a opposite player on a valid field it checks for valid fields in the row below.'''
        jumpPossible=False
        oldrow -= 1
        if (oldrow <=7 and oldrow>=0):
            if (self.boardArray[oldrow][oldcol - 1] == 0):
                if (oldcol - 1 >= 0):
                    self.possMov[oldrow][oldcol - 1] = 1

            if (self.boardArray[oldrow][oldcol - 1] == 1):
                newrow = oldrow - 1
                newcol = oldcol - 2
                if (newrow <= 7 and newrow>=0):
                    if (self.boardArray[newrow][newcol] == 0):
                        self.resetPossMoves()
                        jumpPossible=True
                        self.possMov[newrow][newcol] = 1

            if (oldcol+1 <= 7 and jumpPossible==False):
                if (self.boardArray[oldrow][oldcol+1] == 0):
                    self.possMov[oldrow][oldcol+1] = 1

                elif (self.boardArray[oldrow][oldcol+1] == 1):
                    newrow = oldrow - 1
                    newcol = oldcol + 2
                    if (newrow <= 7 and newrow>=0):
                        if(oldcol<=7):
                            if (self.boardArray[newrow][newcol] == 0 and jumpPossible==False ):
                                self.resetPossMoves()
                                self.possMov[newrow][newcol] = 1


        return self.possMov


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
        '''Method for resetting the game to its initial state.
        It calls the reset arrays methods and it resets the captures variables for each player'''
        self.resetPossMoves()
        self.resetBoardArray()
        self.jumpp1=0
        self.jumpp2=0
        self.update()
        '''clears pieces from the board'''


    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        '''Method for drawing all the squares on the board'''

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

    def ColorSelection(self, color1, color2):
        '''Method for setting the color of the piece of the squares'''
        self.ColorP1=color1
        self.ColorP2=color2


    def drawPossibleMoves(self, painter):
        '''Method for drawing the highlighting of possible fields a piece or a king can move to'''
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
        '''Method for drawing the pieces or a king on the board which are setted in the board array.'''
        painter.setPen(Qt.transparent)
        painter.setBrush(Qt.transparent)
        colTransformation = self.squareWidth()
        rowTransformation = self.squareHeight()
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(col * colTransformation, row * rowTransformation)

                if self.boardArray[row][col] == 1 or self.boardArray[row][col] == 3:
                    painter.setBrush(self.ColorP1)

                elif self.boardArray[row][col] == 2 or self.boardArray[row][col]==4:
                    painter.setBrush(self.ColorP2)

                radiusW = (self.squareWidth() - 2) / 2
                radiusH = (self.squareHeight() - 2) / 2
                center = QPoint(radiusW, radiusH)
                painter.drawEllipse(center, radiusW, radiusH)
                #Drawing the crown
                if self.boardArray[row][col]==3 or self.boardArray[row][col]==4:
                    crown=QColor(212,175,55)
                    painter.setPen(Qt.black)
                    painter.setBrush(crown)
                    painter.drawEllipse(center, radiusW/2,radiusH/2)
                painter.restore()
