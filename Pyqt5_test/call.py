import pro
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QColorDialog, QFontDialog, QFileDialog, QAction, QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from threading import Thread
from time import sleep
import threading
import sqlite3
from sqlite3 import Error
import qstring
import pyqtgraph as pg
from Arduino.ser_receive import *


class Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = pro.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_start.clicked.connect(self.start_graph)
        self.ui.pushButton_stop.clicked.connect(self.stop_graph)

        self.show()

        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.run)
        self.timer1.start()


    def start_graph(self):
        self.ui.pushButton_start.setEnabled(False)
        self.ui.graphicsView_2.start = True

        self.ui.graphicsView_2.start_()

    def stop_graph(self):
        self.ui.pushButton_start.setEnabled(True)
        self.ui.graphicsView_2.start = False

    def run(self):
        if self.ui.graphicsView_2.connection():
            self.ui.pushButton_connection.setText("CONNECTED")
            self.ui.pushButton_connection.setStyleSheet("background-color: rgb(0, 0, 0);\n""color: rgb(0, 255, 0);")
            if not self.ui.pushButton_stop.isEnabled():
                self.ui.pushButton_start.setEnabled(True)
                self.ui.pushButton_stop.setEnabled(True)
        else:
            self.ui.pushButton_connection.setText("DISCONNECTED")
            self.ui.pushButton_connection.setStyleSheet("background-color: rgb(0, 0, 0);\n""color: rgb(255, 255, 0);")
            self.ui.pushButton_start.setEnabled(False)
            self.ui.pushButton_stop.setEnabled(False)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    u = Demo()
    u.show()
    sys.exit(app.exec_())
