from PyQt5.QtWidgets import QDockWidget, QGridLayout, QLabel, QWidget
from PyQt5.QtGui import QPixmap
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
        self.labelP1 = QLabel('Player 1')
        self.labelP2 = QLabel('Player 2')

        self.avatar1= QPixmap("avatarP1.png")
        self.avatar1Label=QLabel('')
        self.avatar1Label.setPixmap(self.avatar1)

        self.avatar2 = QPixmap("avatarP2.png")
        self.avatar2Label = QLabel('')
        self.avatar2Label.setPixmap(self.avatar2)

        grid = QGridLayout()
        grid.addWidget(self.avatar1Label, 0, 0)
        grid.addWidget(self.labelP1, 1, 0)

        grid.addWidget(self.avatar2Label, 2, 0)
        grid.addWidget(self.labelP2, 3, 0)

        self.setLayout(grid)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(grid)
        self.setWidget(self.mainWidget)

        self.show()

    def center(self):
        '''centers the window on the screen'''
