## Todo: implement a simple search engine.
## reference: https://blog.devgenius.io/lets-build-a-search-engine-with-python-3f8dd3320210

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from inspect import getsourcefile

import os, sys, glob, shutil, errno, threading

def copyFolder(src, dst):
    try:
        if os.path.exists(src):
            shutil.copytree(src, dst)
    except OSError as err:
        if err.errno == errno.ENOTDIR:
            shutil.copy2(src, dst)
        else:
            print("default tablist already initiated! happy browsing))")

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

path = os.path.abspath(__file__)
path = os.path.dirname(path)

tablistpath = os.path.join(application_path, 'tablist')
myiconpath = os.path.join(path,'source/images')

copyFolder(os.path.join(path, 'source/tablist'), os.path.join(application_path, 'tablist'))

print("")
print("=============================")
print("")
print(" webbrowser by appstew ")
print("")
print("=============================")
print("")



class outerWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)

        ## for some ambient background, also might be for some watermark-like effect?
        self.label = QLabel('Label', self)
        self.label.setMinimumSize(3840, 2160)
        self.label.setStyleSheet("background-color: rgba(33, 33, 33, 0.33)")
           
        self.vbox = QVBoxLayout(self)
        # below code should not be used
        # self.vbox.addWidget(self.label)

        self.toolbox = QToolBox()
        self.vbox.addWidget(self.toolbox)
        self.toolbox.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 1), stop:0.3 rgba(255, 255, 255, 0.9), stop:1 rgba(255, 255, 255, 0.1))")
        self.toolbox.setFont(QFont("ubuntu", 9,40))
        self.setMinimumSize(400,300)
        
        print(threading.active_count(),"\n", threading.current_thread(),"\n", threading.main_thread(),"\n")


        tabFileList = glob.glob(tablistpath + "/*.tab")
        print(tabFileList)
        self.btn = QPushButton("loads below as tab")
        self.innerbox = QFormLayout()
        self.innerbox.addWidget(self.btn)
        textedit = QTextEdit()
        textedit.append(" ")
        for item in tabFileList:
            textedit.append(item)
            textedit.append(" ")
        self.innerbox.addWidget(textedit)
        widget1 = QWidget()
        widget1.setLayout(self.innerbox)
        self.toolbox.addItem(widget1, "browser")
        

        self.btn.pressed.connect(lambda: self._load(tabFileList))


    def _load(self, tabFileList):
        for file in tabFileList:
            tabFileName = file
            print(tabFileName)
            browser = browserWidget(tabFileName)
            print(browser)
            browser.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
            self.toolbox.addItem(browser, tabFileName)
        print("button pressed")
        self.btn.deleteLater()

        

class browserWidget(QWidget):
    def __init__(self, tabFileName):
        QWidget.__init__(self, None)
        self.tabFileName = tabFileName
        self.setMinimumSize(500,500)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.vbox = QVBoxLayout(self)

        self.tabWidget = QTabWidget()
        self.tabWidget.setDocumentMode(True)
        # self.tabWidget.setStyleSheet("background-color: rgba(192, 191, 188, 0.1);")

        ## buttons
        # unicode characters can be used as below
        # self.back_btn1 = QPushButton("←")
        self.back_btn1 = QPushButton(QIcon(os.path.join(myiconpath, 'back.svg')),"")
        self.back_btn1.pressed.connect(lambda: self.tabWidget.currentWidget().back())
        self.forward_btn = QPushButton(QIcon(os.path.join(myiconpath, 'forward.svg')), "")
        self.forward_btn.pressed.connect(lambda: self.tabWidget.currentWidget().forward())
        self.refresh_btn = QPushButton(QIcon(os.path.join(myiconpath, 'refresh.svg')), "")
        self.refresh_btn.pressed.connect(lambda: self.tabWidget.currentWidget().reload())
        self.home_btn = QPushButton(QIcon(os.path.join(myiconpath, 'home.svg')), "")
        self.home_btn.pressed.connect(lambda: 
                                        self.tabWidget.currentWidget()
                                        .setUrl(QUrl("https://www.google.com")))
        self.urlbar = QLineEdit()
        self.urlbar.setMinimumWidth(500)
        self.urlbar.returnPressed.connect(self.toUrl)
        self.tabWidget.currentChanged.connect(self.current_tab_changed)
        self.add_tab_btn = QPushButton(QIcon(os.path.join(myiconpath, 'plus.svg')),"")
        self.add_tab_btn.pressed.connect(lambda: self.add_new_tab(self.tabWidget, QUrl("https://www.google.com"), self.urlbar))
        self.btnGroup = [self.back_btn1,
                        self.forward_btn,
                        self.refresh_btn,
                        self.home_btn,
                        self.urlbar,
                        self.add_tab_btn]
        
        nav1 = QHBoxLayout()
        nav1.setAlignment(Qt.AlignLeft)
        for i in self.btnGroup:
            i.setMinimumSize(30,30)
            nav1.addWidget(i)
        self.vbox.addLayout(nav1)

        self.setBasicFunction(self.tabWidget)
        self.open_tabs_from_file(self.tabWidget, self.tabFileName, self.urlbar)
        self.vbox.addWidget(self.tabWidget)

        ## for Alt+arrow back function.
        ## ref: https://pynput.readthedocs.io/en/latest/keyboard.html
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            return
        elif event.modifiers() & Qt.AltModifier and event.key() == QtCore.Qt.Key_Left:
            self.tabWidget.currentWidget().back()
            print("back")
        elif event.modifiers() & Qt.AltModifier and event.key() == QtCore.Qt.Key_Right:
            self.tabWidget.currentWidget().forward()
            print("forward")
        elif event.modifiers() & Qt.AltModifier and event.key() == QtCore.Qt.Key_Q:
            # self.tabWidget.currentWidget().forward()
            print("Q key pressed. Killing this tabWidget")
            self.deleteLater()

    def toUrl(self):
        url = QUrl(self.urlbar.text())
        url.setScheme("https")
        self.tabWidget.currentWidget().setUrl(url)
        # self.update_urlbar(url, self.urlbar)

    def current_tab_changed(self, i):
        url = self.tabWidget.currentWidget().url()
        self.update_urlbar(url, self.tabWidget.currentWidget())
        
    def update_urlbar(self, url, browser=None):
        if browser != self.tabWidget.currentWidget():
            return
        self.urlbar.setText(url.toString())
        
    def setBasicFunction(self, tabWidget):
        tabWidget.setMinimumSize(300,300)
        tabWidget.setDocumentMode(True)     
        tabWidget.setTabsClosable(True)
        tabWidget.tabCloseRequested.connect(lambda index: tabWidget.removeTab(index))
        tabWidget.setMovable(True)

    def open_tabs_from_file(self, tabWidget, filepath, urlbar):
        # tabfilenameFull = os.path.join(_filepath, tablistname)
        if filepath!=None:
                
            fr = open(filepath, 'r')
            lines = fr.readlines()
            for line in lines:
                # strip() removes '\n' , which is created by enter key.
                line = line.strip()
                self.add_new_tab(tabWidget, QUrl(line), urlbar)



    def add_new_tab(self, tabWidget, qurl=None, urlbar = QLineEdit, label="Blank"):
        if qurl is None:
            qurl = QUrl("")
        browser = QWebEngineView()
        # browser.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
        browser.setUrl(qurl)
        i = tabWidget.addTab(browser, label)
        tabWidget.setCurrentIndex(i)
        tabWidget.setTabText(i, str(i) + "..loading")
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                    tabWidget.setTabText(
                                        i, browser.page().title()[:5] + " .. "))

# add arguments here
args = sys.argv
args.append("--ignore-gpu-blocklist")
args.append("--no-sandbox")
app = QtWidgets.QApplication(args)
if __name__ == "__main__":
    window = outerWidget()
    # global opacity
    # window.setWindowOpacity(.95)
    window.show()
    app.exec_()




