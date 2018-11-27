from PyQt5.QtWidgets import QDockWidget, QGridLayout,QLabel, QWidget
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
        self.labelP1= QLabel('Player 1')
        self.labelP2 = QLabel('Player 2')

        grid = QGridLayout()
        grid.addWidget(self.labelP1, 0, 0)
        grid.addWidget(self.labelP2, 1, 0)
        
        self.setLayout(grid)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(grid)
        self.setWidget(self.mainWidget)

        self.show()

    def center(self):
        '''centers the window on the screen'''
