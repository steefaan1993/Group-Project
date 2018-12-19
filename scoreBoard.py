from PyQt5.QtWidgets import QDockWidget, QGridLayout, QLabel, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot
from board import Board
import sys


class ScoreBoard(QDockWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')
        self.timerLabel = QLabel('Player1 Timer: ')
        self.pTimerLabel = QLabel('Player2 Timer: ')
        self.labelP1 = QLabel('Player 1')
        self.labelP2 = QLabel('Player 2')
        self.turnLabelP1 = QLabel("<font color='red'><strong>Your Turn</strong></font>")
        self.turnLabelP2 = QLabel("")
        self.captureP1 = QLabel('Captures: 0')
        self.captureP2 = QLabel('Captures: 0')
        self.remainingP1 = QLabel('Remaining: 12')
        self.remainingP2 = QLabel('Remaining: 12')
        self.space1 = QLabel("<font color='green'>---------</font>")
        self.space2 = QLabel("<font color='green'>---------</font>")
        self.space3 = QLabel("<font color='green'>---------</font>")
        self.space4 = QLabel("<font color='green'><strong>---------</strong></font>")

        self.avatar1= QPixmap("./img/yellow.png")
        self.avatar1Label=QLabel('')
        self.avatar1Label.setPixmap(self.avatar1)

        self.avatar2 = QPixmap("./img/red.png")
        self.avatar2Label = QLabel('')
        self.avatar2Label.setPixmap(self.avatar2)

        self.space1.resize(70,70)
        self.space2.resize(70, 70)
        grid = QGridLayout()


        grid.addWidget(self.avatar1Label, 1, 0)
        grid.addWidget(self.labelP1, 1,1)
        grid.addWidget(self.timerLabel, 2, 0)
        grid.addWidget(self.turnLabelP1, 2, 1)
        grid.addWidget(self.captureP1, 3, 0)
        grid.addWidget(self.remainingP1, 4, 0)
        grid.addWidget(self.space3, 5, 0)
        grid.addWidget(self.space4, 5, 1)

        grid.addWidget(self.avatar2Label,6, 0)
        grid.addWidget(self.labelP2, 6, 1)
        grid.addWidget(self.pTimerLabel, 7, 0)
        grid.addWidget(self.turnLabelP2, 7, 1)
        grid.addWidget(self.captureP2, 8, 0)
        grid.addWidget(self.remainingP2, 9, 0)


        self.setLayout(grid)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(grid)
        self.setWidget(self.mainWidget)

        self.show()

    def center(self):
        '''centers the window on the screen'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)
        board.updatepTimerSignal.connect(self.setpTimeRemaining)
        board.updatepTurnSignal.connect(self.setTurnLabel)
        board.updatePlayers.connect(self.setPlayerStats)

    @pyqtSlot(str) # checks to make sure that the following slot is receiving an arguement of the right type
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location:" + clickLoc)
        print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining'''
        sr = timeRemaining % 60
        mr = timeRemaining // 60

        update = "Player1 Timer: " + str(mr) + ":" + str(sr)
        self.timerLabel.setText(update)
        print('slot '+update)
        #self.redraw()
        if Board.counter == 0:
            self.timerLabel.setText("GameOver")
            self.gameover("Player one")

    @pyqtSlot(int)
    def setpTimeRemaining(self, pTimeRemaining):
        sr = pTimeRemaining % 60
        mr = pTimeRemaining // 60
        update2 = "Player2 Timer: " + str(mr) + ":" + str(sr)
        self.pTimerLabel.setText(update2)
        print('slot ' + update2)
        if Board.pCounter == 0:
            self.timerLabel.setText("GameOver")
            self.gameover("Player two")


    @pyqtSlot(int)
    def setTurnLabel(self, tmp):
        if tmp == 1:
            self.turnLabelP1.setText(" ")
            self.turnLabelP2.setText("<font color='red'><strong>Your Turn</strong></font>")
        else:
            self.turnLabelP2.setText(" ")
            self.turnLabelP1.setText("<font color='red'><strong>Your Turn</strong></font>")

    @pyqtSlot(int, int)
    def setPlayerStats(self, j1, j2):
        self.captureP1.setText("Captures: " + str(j1))
        self.remainingP1.setText("Remaining: " + str(12-j2))
        self.captureP2.setText("Captures: " + str(j2))
        self.remainingP2.setText("Remaining: " + str(12 - j1))

    def seticon(self, p1, p2):
        player1 = p1.lower()
        player2 = p2.lower()
        self.avatar1.load("./img/" + player1 + ".png")
        self.avatar1Label.setPixmap(self.avatar1)
        self.avatar2.load("./img/" + player2 + ".png")
        self.avatar2Label.setPixmap(self.avatar2)
        self.update()

    def gameover(self, player):
        QMessageBox.information(self, "Message", "%s has lost because he has no time left " %player)





