from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QAction, QMessageBox, QInputDialog
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
        gameMenu = mainMenu.addMenu(" Game")

        pauseAction = QAction(QIcon("./img/pause.png"), "Pause Game", self)
        gameMenu.addAction(pauseAction)
        pauseAction.triggered.connect(self.tboard.pause)

        playAction = QAction(QIcon("./img/play.png"), "Play Game", self)
        gameMenu.addAction(playAction)
        playAction.triggered.connect(self.tboard.start)

        resetAction = QAction(QIcon("./img/reset.png"), "Reset", self)
        gameMenu.addAction(resetAction)
        resetAction.triggered.connect(self.tboard.resetGame)

        exitAction = QAction(QIcon("./img/exit.png"), "Exit", self)
        gameMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exit)

        helpMenu = mainMenu.addMenu("Help")
        help = helpMenu.addMenu(QIcon("./img/help.png")," Help")
        htp = help.addMenu("How To Play")

        rulesAction = QAction( "Rules", self)
        help.addAction(rulesAction)
        rulesAction.triggered.connect(self.rules)

        about = QAction(QIcon("./img/about.png"), "About", self)
        helpMenu.addAction(about)
        about.triggered.connect(self.about)

        howtoplay = QAction(QIcon("./img/checkers.png"), "How To Play", self)
        htp.addAction(howtoplay)
        howtoplay.triggered.connect(self.htpHelp)

        pause = QAction(QIcon("./img/pause.png"), "Pause", self)
        htp.addAction(pause)
        pause.triggered.connect(self.pauseHelp)

        play = QAction(QIcon("./img/play.png"), "Play", self)
        htp.addAction(play)
        play.triggered.connect(self.playHelp)

        reset = QAction(QIcon("./img/reset.png"), "Reset", self)
        htp.addAction(reset)
        reset.triggered.connect(self.resetHelp)

        exit = QAction(QIcon("./img/exit.png"), "Exit", self)
        htp.addAction(exit)
        exit.triggered.connect(self.exitHelp)

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
        self.option()


    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def option(self):
        items = ("Red", "Blue", "Green", "Yellow", "Pink")
        item, okPressed = QInputDialog.getItem(self, "Options", "Player1 Colour:", items, 0, False)
        if okPressed and item:
            print(item)
        else:
            item = "Yellow"
        if item == "Red":
            player1colour = Qt.red

            items2 = ("Blue", "Yellow")
        elif item == "Blue":
            player1colour = Qt.blue
            items2 = ("Red", "Green", "Yellow", "Pink")
        elif item == "Yellow":
            player1colour = Qt.yellow
            items2 = ("Red", "Green", "Blue", "Pink")
        elif item == "Pink":
            player1colour = Qt.magenta
            items2 = ("Green", "Yellow", "Blue")
        else:
            player1colour = Qt.green
            items2 = ("Blue", "Yellow", "Pink")
        item2, okPressed = QInputDialog.getItem(self, "Options", "Player2 Colour:", items2, 0, False)
        if okPressed and item2:
            print(item2)
        else:
            item2 = "Red"
        if item2 == "Red":
            player2colour = Qt.red
        elif item2 == "Blue":
            player2colour = Qt.blue
        elif item2 == "Yellow":
            player2colour = Qt.yellow
        elif item2 == "Pink":
            player2colour = Qt.magenta
        else:
            player2colour = Qt.green
        self.tboard.ColorSelection(player1colour, player2colour)
        self.scoreBoard.seticon(item, item2)
        self.tboard.start()

    def exit(
            self):  # it's an option for users to pick to exit. It'll automatically get connected to the closeEvent method down below.
        self.close()

        # CLOSE EVENT METHOD FOR CLICKING THE 'X' BUTTON

    def closeEvent(self, event):  # a window to pop up when the user wants to exit using 'X' button.
        # window asks the user if they're sure to exit and give them options to say yes, save or cancel.
        # selecting yes will close the app.
        # selecting save will get connected to the save method and check if user actually saved the file. If they didn't it won't close the application.
        # selecting cancel will ignore the request and keep the application open.
        close = QMessageBox()
        close.setWindowTitle("Exit")
        close.setWindowIcon(QIcon("./img/exit.png"))
        close.setText("Are you sure you want to quit?\n")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def rules(self):
        help = QMessageBox()
        help.setWindowTitle("Rules")
        help.setWindowIcon(QIcon("./img/checkers.png"))
        help.setText("1) Each Player start with 12 pieces.\n 2) Pieces can only move diagonally and forward (only one square).\n 3) Captures are made by jumping over an enemy piece.\n 4) If you make a capture, you can keep playing.\n 5) A piece becomes a king if it reaches to the enemy side.\n 6) A king can move forwards and backwards.\n 7) A Player wins if the opponent runs out of time or if the Player captures all 12 enemy pieces in time.\n")
        help.setStandardButtons(QMessageBox.Ok)
        help = help.exec()

    def pauseHelp(self):
        help = QMessageBox()
        help.setWindowTitle("Pause")
        help.setWindowIcon(QIcon("./img/pause.png"))
        help.setText("This button allows you to pause the game once you started.\n")
        help.setStandardButtons(QMessageBox.Ok)
        help = help.exec()

    def playHelp(self):
        help = QMessageBox()
        help.setWindowTitle("Play")
        help.setWindowIcon(QIcon("./img/play.png"))
        help.setText("This button allows you to start the game after you pause it.\n")
        help.setStandardButtons(QMessageBox.Ok)
        help = help.exec()

    def resetHelp(self):
        help = QMessageBox()
        help.setWindowTitle("Reset")
        help.setWindowIcon(QIcon("./img/reset.png"))
        help.setText("This button allows you to reset the timers, the stats, and the position of the pieces.\n")
        help.setStandardButtons(QMessageBox.Ok)
        help = help.exec()

    def exitHelp(self):
        help = QMessageBox()
        help.setWindowTitle("Exit")
        help.setWindowIcon(QIcon("./img/exit.png"))
        help.setText("This button allows you to exit the application.\n")
        help.setStandardButtons(QMessageBox.Ok)
        help = help.exec()

    def htpHelp(self):
        help = QMessageBox()
        help.setWindowTitle("How To Play")
        help.setWindowIcon(QIcon("./img/checkers.png"))
        help.setText("If the score board says it's your turn, you can move by clicking on a piece. The application will highlight the available squares to move. You can pause, start, reset and exit by clicking the Game menu in the menu bar. Hope you'll enjoy it!\n")
        help.setStandardButtons(QMessageBox.Ok)
        help = help.exec()

    def about(self):
        help = QMessageBox()
        help.setWindowTitle("About")
        help.setWindowIcon(QIcon("./img/about.png"))
        help.setText("This application is a Draughts game (aka Checkers) made by Ecem Oral 2929807 and Stefan Wirtz 2981467.\n")
        help.setStandardButtons(QMessageBox.Ok)
        help = help.exec()

