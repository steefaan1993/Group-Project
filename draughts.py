from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from board import Board
from scoreBoard import ScoreBoard
import sys

class Draughts(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        '''initiates application UI'''
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)
        # SETTING UP MENU BAR
        mainMenu = self.menuBar()

        # SETTING UP TWO MENUS IN MENU BAR
        fileMenu = mainMenu.addMenu(" File")
        fileMenu.addAction(QIcon("./img/settings.png"), "Options")
        fileMenu.addAction(QIcon("./img/reset.png"), "Reset")
        fileMenu.addAction(QIcon("./img/exit.png"), "Exit")
        helpMenu = mainMenu.addMenu("Help")
        help = helpMenu.addMenu(QIcon("./img/help.png")," Help")
        help.addAction( "How To Play")
        help.addAction( "Rules")
        helpMenu.addAction(QIcon("./img/about.png"), "About")

        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)
        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)
        self.scoreBoard.make_connection(self.tboard)

        self.tboard.start()

        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Draughts')
        self.setWindowIcon(QIcon("./img/checkers.png"))
        self.show()


    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
