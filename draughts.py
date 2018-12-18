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
        fileMenu = mainMenu.addMenu(" File")
        optionAction = QAction(QIcon("./img/settings.png"), "Options", self)
        fileMenu.addAction(optionAction)
        optionAction.triggered.connect(self.option)

        resetAction = QAction(QIcon("./img/reset.png"), "Reset", self)
        fileMenu.addAction(resetAction)
        resetAction.triggered.connect(self.tboard.resetGame)

        exitAction = QAction(QIcon("./img/exit.png"), "Exit", self)
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exit)

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
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Save | QMessageBox.Cancel)
        close = close.exec()
        if close == QMessageBox.Yes:
            event.accept()
       # elif close == QMessageBox.Save:
        #    save = self.save()
         #   if save == False:
          #      event.ignore()
           # else:
            #    event.accept()
        else:
            event.ignore()
