#!/usr/bin/env python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests as r
import os

class App(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        self.setApplicationName('Song Serve')
        self.mainWindow = MainWindow()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Song Serve UI')
        
