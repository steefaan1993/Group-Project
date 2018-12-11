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
        self.labelP1 = QLabel('Player 1')
        self.labelP2 = QLabel('Player 2')
        self.turnLabelP1 = QLabel('Your Turn')
        self.turnLabelP2 = QLabel('')
        self.captureP1 = QLabel('Captures: ')
        self.captureP2 = QLabel('Captures: ')
        self.remainingP1 = QLabel('Remaining: ')
        self.remainingP2 = QLabel('Remaining: ')
        self.space1 = QLabel('---------')
        self.space2 = QLabel('---------')
        self.space3 = QLabel('---------')
        self.space4 = QLabel('---------')

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
        grid.addWidget(self.space1, 1, 0)
        grid.addWidget(self.space2, 1, 1)
        grid.addWidget(self.avatar1Label, 2, 0)
        grid.addWidget(self.labelP1, 2,1)
        grid.addWidget(self.turnLabelP1, 3, 1)
        grid.addWidget(self.captureP1, 4, 0)
        grid.addWidget(self.remainingP1, 5, 0)
        grid.addWidget(self.space3, 6, 0)
        grid.addWidget(self.space4, 6, 1)

        grid.addWidget(self.avatar2Label,7, 0)
        grid.addWidget(self.labelP2, 7, 1)
        grid.addWidget(self.turnLabelP2, 8, 1)
        grid.addWidget(self.captureP2, 9, 0)
        grid.addWidget(self.remainingP2, 10, 0)


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

    @pyqtSlot(str) # checks to make sure that the following slot is receiving an arguement of the right type
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location:" + clickLoc)
        print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining'''
        update = "Timer: " + str(timeRemaining)
        self.timerLabel.setText(update)
        print('slot '+update)
        #self.redraw()
        if Board.counter == 0:
            self.timerLabel.setText("GameOver")
