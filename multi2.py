from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QMainWindow
import sys

from random import randint
from browser import outerWidget
import embed2image

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)

class Container(QtWidgets.QTabWidget):
    def __init__(self):
        QtWidgets.QTabWidget.__init__(self)

        # bg_img = os.path.join(path, 'source/images/terminal_logo.svg')
        # bg_img2 = os.path.join(path, 'source/images/about_logo.svg')

        HomeWidget = QWidget()
        # HomeWidget.setStyleSheet("background-color: rgba(77, 77, 77, 0.90);")
        HomeWidget.setStyleSheet("""background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0 
                                 stop:0 rgba(55, 55, 55, 0.99),
                                 stop:0.45 rgba(55, 55, 55, 0.8),
                                 stop:0.55 rgba(55, 55, 55, 0.8),
                                 stop:1 rgba(55, 55, 55, 0.99));
                                 """
                                 """
                                 background-repeat:no-repeat;
                                 background-position: center;
                                 background-image:url(%s);
                                 """
                                 % ":/icons/bg_img2")
  
        terminal = Terminal()
        self.processList = []
        self.addTab(HomeWidget, "Home")
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setDocumentMode(True)
        self.setTabsClosable(True)
        self.addTab(terminal, "term")
        self.addTab(outerWidget(), "browser")
        self.resize(500, 400)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(Container())
        self.resize(800, 600)

    def show_new_window(self, checked):
        if self.w is None:
            self.w = outerWidget()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()