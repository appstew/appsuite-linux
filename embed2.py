#!/usr/bin/env python3
# (same code seems to run both with python3 and python2 with PyQt5 in Ubuntu 18.04.3 LTS)
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import QProcess, QStandardPaths, Qt, QEvent, QSettings, QPoint, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QPlainTextEdit, QVBoxLayout, QMainWindow
import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck, Gdk
import os, time, signal
import embed2image

path = os.path.abspath(__file__)
path = os.path.dirname(path)
os.chdir(path)

#tkinter tutorial 
# how to make money developing apps & app monetization model
# https://appetiser.com.au/blog/how-do-free-apps-make-money/
# https://appetiser.com.au/blog/app-monetization/
# Fareedkhandev, TomSchimansky, flask, tkinter
# https://medium.com/@fareedkhandev/modern-gui-using-tkinter-12da0b983e22
# https://medium.com/@fareedkhandev/create-desktop-application-using-flask-framework-ee4386a583e9
# various & many method to package python app: flask, cython, linuxdeployqt, appimage-builder, python utils etc
# https://stackoverflow.com/questions/261638/how-do-i-protect-python-code-from-being-read-by-users
# 기존의 appimage 는 portability 라는 장점 외에는 잘해야 리눅스 진영에서만 호환이 된다는 특징이 있었다.
# cython 으로 build 해도 cross-platform이 되기 위해선 vagrant나 docker 를 별도로 써야 한다고? 더 간편한 방법은 없을까?
# 이 아티클(https://medium.com/@xpl/protecting-python-sources-using-cython-dcd940bb188e) 과 유저(https://github.com/xpl/panic-overlay)
# 는 상대적으로 잦은 빌드와 배포 주기를 가진 앱은 travis-ci 가 유리할 수도 있다고 설명한다.
# https://gall.dcinside.com/board/view/?id=programming&no=1322392
# 희망편 https://gall.dcinside.com/mgallery/board/view/?id=github&no=52180
# cpython 자세히 : https://www.sktenterprise.com/bizInsight/blogDetail/dev/2434

path = os.path.abspath(__file__)
path = os.path.dirname(path)

# tkterminal and stdout
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
  
        self.processList = []
        self.addTab(HomeWidget, "Home")
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setDocumentMode(True)
        self.setTabsClosable(True)
        
        self.setMovable(True)
        # self.embed(path + '/urxvt', [], 'urxvt')
        # self.embed('nautilus', [], 'urxvt')
        self.embed('python', [path +'/browser.py'], 'browser')
        # self.embed('python', ['./browser.py'], 'browser')
   

    def embed(self, command, args, name):
        proc = QtCore.QProcess()
        proc.setProgram(command)
        proc.setArguments(args)
        proc.setObjectName(name)
        #started, procId = proc.startDetached()
        #pid = None
        #started = proc.startDetached(pid)
        # https://stackoverflow.com/q/31519215 : "overload" startDetached : give three arguments, get a tuple(boolean,PID)
        # NB: we will get a failure `xterm: No absolute path found for shell: .` even if we give it an empty string as second argument; must be a proper abs path to a shell
        started, procId = proc.startDetached()
        ## procId 는 pid 이고, 아래의 w.get_pid()가 tid(LWP, Thread Id) 임
        # started, procId = proc.start()
        
        if not started:
            # QtWidgets.QMessageBox.warning(self, "app not found", ' "{}" not found. processing next app..'.format(command))
            return
        attempts = 0
        ## 대충 이런 느낌이다. 실제 tid(LWP) = Wnck.Screen.get_default().get_windows().get_pid()
        ## pgrep browserpython 으로 구할 수 있다.
        ## 프로세스 시작 > procId(LWP) 생성됨 > Wnck.Screen.get_default().get_windows() 로 pid 를 구한다.(15번) > 
        ## 이후 일치하면 
        ## QtWidgets.QWidget.createWindowContainer(QtGui.QWindow.fromWinId(w.get_xid()))
        ## w <- Wnck.Screen.get_default().get_windows()
        while attempts < 11:
            screen = Wnck.Screen.get_default()
            screen.force_update()
            
            # do a bit of sleep, else window is not really found
            time.sleep(.33)
            # this is required to ensure that newly mapped window get listed.
            while Gdk.events_pending():
                Gdk.event_get()
            for w in screen.get_windows():
                print(attempts, " || w.get_pid() : " + str(w.get_pid()), "procId : " + str(procId) + " || ", w.get_pid() == procId)
                if w.get_pid() == procId:
                    print("")
                    print(" ==== ")
                    print("")
                    print("pid or procId is : " + str(w.get_pid()))
                    print("")
                    print("now appending self.processList[]..")
                    self.processList.append(procId)
                    print("")
                    print("self.processList[] is now : ")
                    print("w is: %d", w)
                    print("w.get_xid is: %d", w.get_xid())
                    print(w.get_application().get_name())
                    print(w.get_session_id())
                    print(self.processList)
                    print("")
                    print(" ==== ")
                    print("")

            
                    proc.setParent(self)
      
                    win32w = QtGui.QWindow.fromWinId(w.get_xid()) # this finally works
                    win32w.setFlags(QtCore.Qt.FramelessWindowHint)
                    widg = QtWidgets.QWidget.createWindowContainer(win32w)
                    time.sleep(0.33)
                    self.addTab(widg, name)
      
                    self.resize(500, 400) # set initial size of window
                    return
            attempts += 1
        # QtWidgets.QMessageBox.critical(self, 'Window not found, or process not started properly')

    def closeEvent(self, event):
        print("closing App")
        ## killing child process.
        ## there is another method using subprocess.terminate(), psutil.process_iter()
        for pid in self.processList:
            os.kill(pid, signal.SIGTERM)
            print("terminating process pid : " + str(pid))
        

app = QtWidgets.QApplication(sys.argv)
w = Container()
w.show()
sys.exit(app.exec_())