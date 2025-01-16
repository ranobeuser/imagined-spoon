import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QMainWindow, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,QStackedLayout,QLineEdit,QTimeEdit,QLCDNumber)

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget

from PyQt5 import QtCore

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Задание 2: изменение текста")
        
        Layout = QVBoxLayout()
        Layout1 = QVBoxLayout()
        Layout2 = QVBoxLayout()
        
        widget = QWidget()
        widget.setLayout(Layout)
        
        Layout.addLayout(Layout1)
        Layout.addLayout(Layout2)
        
        self.labelText = "Этот текст приснится мне в кошмарах!"
        
        self.textLabel = QLabel(f"{self.labelText}")
        self.textLabel.setAlignment(QtCore.Qt.AlignCenter)
        Layout1.addWidget(self.textLabel)
        
        colorComboBox = QComboBox()
        colorComboBox.addItems(["черный", "красный", "синий"])
        colorComboBox.currentIndexChanged.connect(self.ChangeColor)
        
        Layout2.addWidget(colorComboBox)
        
        self.setCentralWidget(widget)
         # Button = QPushButton("Name")
         # Button.clicked.connect(self.Click)
         # self.findChild(QLineEdit).setText(str(result))
    
    def Click(self):
        button = self.sender()
        text = button.text()
        
    def ChangeColor(self):
        print("hi")
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
