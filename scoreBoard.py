from PyQt5.QtWidgets import QDockWidget, QGridLayout, QLabel, QWidget
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
        self.timerLabel = QLabel('Timer: ')
        self.pTimerLabel = QLabel('Player Timer: ')
        self.labelP1 = QLabel('Player 1')
        self.labelP2 = QLabel('Player 2')
        self.turnLabelP1 = QLabel("<font color='red'><strong>Your Turn</strong></font>")
        self.turnLabelP2 = QLabel('')
        self.captureP1 = QLabel('Captures: ')
        self.captureP2 = QLabel('Captures: ')
        self.remainingP1 = QLabel('Remaining: ')
        self.remainingP2 = QLabel('Remaining: ')
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
        grid.addWidget(self.timerLabel, 0, 0)
        grid.addWidget(self.pTimerLabel, 1, 0)
        grid.addWidget(self.space1, 2, 0)
        grid.addWidget(self.space2, 2, 1)
        grid.addWidget(self.avatar1Label, 3, 0)
        grid.addWidget(self.labelP1, 3,1)
        grid.addWidget(self.turnLabelP1, 4, 1)
        grid.addWidget(self.captureP1, 5, 0)
        grid.addWidget(self.remainingP1, 6, 0)
        grid.addWidget(self.space3, 7, 0)
        grid.addWidget(self.space4, 7, 1)

        grid.addWidget(self.avatar2Label,8, 0)
        grid.addWidget(self.labelP2, 8, 1)
        grid.addWidget(self.turnLabelP2, 9, 1)
        grid.addWidget(self.captureP2, 10, 0)
        grid.addWidget(self.remainingP2, 11, 0)


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

        update = "Timer: " + str(mr) + ":" + str(sr)
        self.timerLabel.setText(update)
        print('slot '+update)
        #self.redraw()
        if Board.counter == 0:
            self.timerLabel.setText("GameOver")

    @pyqtSlot(int)
    def setpTimeRemaining(self, pTimeRemaining):
        update2 = "Player Timer: " + str(pTimeRemaining)
        self.pTimerLabel.setText(update2)
        print('slot ' + update2)
        # self.redraw()

    def seticon(self, p1, p2):
        player1 = p1.lower()
        player2 = p2.lower()
        self.avatar1.load("./img/" + player1 + ".png")
        self.avatar1Label.setPixmap(self.avatar1)
        self.avatar2.load("./img/" + player2 + ".png")
        self.avatar2Label.setPixmap(self.avatar2)
        self.update()


