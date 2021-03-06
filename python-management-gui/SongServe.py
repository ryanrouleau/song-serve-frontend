#!/usr/bin/env python3

from NodeServerThread import NodeServerThread
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests as r
import sys, time, webbrowser


class App(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        QFontDatabase.addApplicationFont('./fonts/Raleway-Regular.ttf')
        QFontDatabase.addApplicationFont('./fonts/Raleway-Bold.ttf')
        QFontDatabase.addApplicationFont('./fonts/Raleway-ExtraBold.ttf')
        self.setApplicationName('Song Serve UI')
        self.mainWindow = MainWindow()
        self.mainWindow.show()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setStyleSheet('font-family: "Raleway"')
        self.setWindowTitle('Song Serve UI')
        self.nodeThread = NodeServerThread()
        self.mainWidget = MainWidget(self.nodeThread)
        self.setCentralWidget(self.mainWidget)

    def closeEvent(self, event):
        # exiting thread always throws error.  We're just silencing it
        try:
            self.nodeThread.exitServer()
        except:
            pass


class MainWidget(QWidget):
    def __init__(self, nodeThread):
        QWidget.__init__(self)
        self.setObjectName('MainWidget')
        self.mainLayout = QVBoxLayout(self)

        self.title = QLabel('Manage Your Library')
        self.title.setStyleSheet('font-size: 32px; font-weight: 700')
        self.title.setAlignment(Qt.AlignCenter)

        self.dirInfo = None
        try:
            self.dirInfo = r.get('http://localhost:3000/api/manage').json()
        except:
            print('\n Song Serve server not running.  Starting in new thread...\n')
            nodeThread.start()

        # keep trying to hit server until it's responding
        timeElapsed = 0
        while self.dirInfo == None:
            time.sleep(0.25)
            try:
                timeElapsed += 0.25
                self.dirInfo = r.get('http://localhost:3000/api/manage').json()
            except:
                if timeElapsed > 2.5:
                    sys.exit(1)
                pass

        self.dirList = DirList(self.dirInfo['dirs'])

        self.addBttn = QPushButton('Add A Directory')
        self.addBttn.clicked.connect(self.addDir)

        self.removeBtttn = QPushButton('Remove Selected Directory')
        self.removeBtttn.clicked.connect(self.removeDir)

        self.bttnLayout = QHBoxLayout()
        self.bttnLayout.addWidget(self.addBttn)
        self.bttnLayout.addWidget(self.removeBtttn)

        self.openPlayerBttn = QPushButton('Open Music Player')
        self.openPlayerBttn.clicked.connect(self.openPlayerInBrowser)

        self.infoLayout = QHBoxLayout()
        self.infoLayout.setContentsMargins(10,0,0,0)
        self.infoCards = {
            'Directories': InfoCard('Directories', self.dirInfo['numDirs']),
            'Albums': InfoCard('Albums', self.dirInfo['numAlbums']),
            'Artists': InfoCard('Artists', self.dirInfo['numArtists']),
            'Songs': InfoCard('Songs', self.dirInfo['numSongs'])
        }
        self.infoLayout.addWidget(self.infoCards['Directories'])
        self.infoLayout.addWidget(self.infoCards['Albums'])
        self.infoLayout.addWidget(self.infoCards['Artists'])
        self.infoLayout.addWidget(self.infoCards['Songs'])

        self.progressLabel = QLabel('')
        self.progressLabel.setAlignment(Qt.AlignCenter)
        self.progressLabel.setContentsMargins(0,5,0,5)

        self.mainLayout.addWidget(self.title)
        self.mainLayout.addWidget(self.dirList)
        self.mainLayout.addLayout(self.bttnLayout)
        self.mainLayout.addWidget(self.openPlayerBttn)
        self.mainLayout.addLayout(self.infoLayout)
        self.mainLayout.addWidget(Seperator())
        self.mainLayout.addWidget(self.progressLabel)

        self.mainLayout.addStretch()

    def addDir(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder", QDir.homePath());
        self.progressLabel.setText('Adding {} to library...'.format(path))
        if path == '': return
        self.dirList.add(path)
        self.updateInfoCards()
        self.progressLabel.setText('Added {} to library.'.format(path))

    def removeDir(self):
        path = self.dirList.currentItem().text()
        self.progressLabel.setText('Removing {} from library...'.format(path))
        self.dirList.remove(path)
        self.updateInfoCards()
        self.progressLabel.setText('Removed {} from library.'.format(path))

    def updateInfoCards(self):
        resp = r.get('http://localhost:3000/api/manage').json()
        self.infoCards['Albums'].bigNum.setText(str(resp['numAlbums']))
        self.infoCards['Artists'].bigNum.setText(str(resp['numArtists']))
        self.infoCards['Songs'].bigNum.setText(str(resp['numSongs']))
        self.infoCards['Directories'].bigNum.setText(str(resp['numDirs']))

    def openPlayerInBrowser(self):
        webbrowser.open('http://localhost:3000')


class DirList(QListWidget):
    def __init__(self, dirs):
        QListWidget.__init__(self)
        self.dirs = dirs
        dirs.sort(key=lambda x: x['dirId'])
        for dirObj in dirs:
            self.addItem(dirObj['absolutePath'])


    def add(self, path):
        url = 'http://localhost:3000/api/manage'
        payload = {'absolutePath': path}
        resp = r.put(url, json=payload).json()
        if 'err' in resp:
            ErrDiag(resp['err'])
            return

        self.dirs.append({'absolutePath': path, 'dirId': resp['dirId']})
        self.addItem(path)
        AddDiag(resp, path)


    def remove(self, path):
        i = self.findIndex(path)

        url = 'http://localhost:3000/api/manage'
        payload = {'dirId': self.dirs[i]['dirId']}
        resp = r.delete(url, json=payload).json()
        if 'err' in resp:
            ErrDiag(resp['err'])
            return

        self.takeItem(i)
        del self.dirs[i]
        RemoveDiag(resp, path)


    def findIndex(self, path):
        index = -1
        for i in range(0, len(self.dirs)):
            if (self.dirs[i]['absolutePath'] == path):
                index = i
                return index
        return index


class ErrDiag(QMessageBox):
    def __init__(self, errMsg):
        QMessageBox.__init__(self)
        self.errDiag = QMessageBox(self)
        self.errDiag.setIcon(QMessageBox.Warning)
        self.errDiag.setText(errMsg)
        self.errDiag.exec_()
        return


class RemoveDiag(QDialog):
    def __init__(self, resp, path):
        QDialog.__init__(self)
        self.setWindowTitle('Removed {}'.format(path))
        self.mainLayout = QVBoxLayout(self)
        self.title = QLabel('Successfully Removed:')
        self.title.setStyleSheet('font-size: 22px; font-weight: 600');
        self.infoLayout = QHBoxLayout()
        self.infoLayout.addWidget(InfoCard('Albums', resp['numAlbumsDeleted']))
        self.infoLayout.addWidget(InfoCard('Artists', resp['numArtistsDeleted']))
        self.infoLayout.addWidget(InfoCard('Songs', resp['numSongsDeleted']))
        self.closeBttn = QPushButton('Close')
        self.closeBttn.clicked.connect(self.accept)
        self.mainLayout.addWidget(self.title)
        self.mainLayout.addLayout(self.infoLayout)
        self.mainLayout.addWidget(self.closeBttn)
        self.exec_()


class AddDiag(QDialog):
    def __init__(self, resp, path):
        QDialog.__init__(self)
        self.setWindowTitle('Added {}'.format(path))
        self.mainLayout = QVBoxLayout(self)
        self.title = QLabel('Successfully Added:')
        self.title.setStyleSheet('font-size: 22px; font-weight: 600');
        self.infoLayout = QHBoxLayout()
        self.infoLayout.addWidget(InfoCard('Albums', resp['numAlbumsAdded']))
        self.infoLayout.addWidget(InfoCard('Artists', resp['numArtistsAdded']))
        self.infoLayout.addWidget(InfoCard('Songs', resp['numSongsAdded']))
        self.closeBttn = QPushButton('Close')
        self.closeBttn.clicked.connect(self.accept)
        self.mainLayout.addWidget(self.title)
        self.mainLayout.addLayout(self.infoLayout)
        self.mainLayout.addWidget(self.closeBttn)
        self.exec_()


class InfoCard(QWidget):
    def __init__(self, type, num):
        QWidget.__init__(self)
        self.mainLayout = QVBoxLayout(self)
        self.bigNum = QLabel(str(num))
        self.bigNum.setStyleSheet('font-size: 22px; font-weight:600')
        self.bigNum.setAlignment(Qt.AlignCenter)
        self.label = QLabel(type)
        self.label.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.bigNum)
        self.mainLayout.addWidget(self.label)


class Seperator(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.setFrameShape(QFrame.HLine)
        self.setStyleSheet('border: 0px; border-bottom: 1px solid #2e2e2e')

if __name__ == '__main__':
    app = App()
    sys.exit(app.exec_())
