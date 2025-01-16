import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,QStackedLayout,QLineEdit,QTimeEdit,QLCDNumber)

from PyQt5.QtGui import QColor, QPalette
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

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

        self.setWindowTitle("Калькулятор")
        buttons  = ["7","8","9","/","4","5","6","*","1","2","3","-","0",".","%","+"]
        i=0

        Layout = QVBoxLayout()
        Layout1 = QVBoxLayout()
        Layout2 = QGridLayout()

        widget = QWidget()
        widget.setLayout(Layout)

        Layout.addLayout(Layout1)
        Layout1.addWidget(QLineEdit())
        Layout1.addLayout(Layout2)

        for x in range(4):
                for y in range(4):
                        butt = QPushButton(buttons[i])
                        butt.clicked.connect(self.Click)
                        
                        Layout2.addWidget(butt,x,y)
                        i+=1

        delButt = QPushButton("Del")
        delButt.clicked.connect(self.Click)
        Layout2.addWidget(delButt,5,0)

        CButt = QPushButton("C")
        CButt.clicked.connect(self.Click)
        Layout2.addWidget(CButt,5,1)

        evalButt = QPushButton("Ввод")
        evalButt.clicked.connect(self.Click)
        Layout2.addWidget(evalButt,5,2,1,2)

        self.setCentralWidget(widget)

    def Click(self):
        button = self.sender()
        text = button.text()
        
        if text == "Ввод":
            try:
                expression = self.findChild(QLineEdit).text()
                result = eval(expression)
                self.findChild(QLineEdit).setText(str(result))
            except:
                pass
        elif text == "C":
            self.findChild(QLineEdit).setText("")

        elif text == "Del":
             theText = str(self.findChild(QLineEdit).text())
             self.findChild(QLineEdit).setText(theText[:-1])

        else:
            self.findChild(QLineEdit).insert(text)

app=QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
