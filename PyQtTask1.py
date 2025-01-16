import sys

from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QMainWindow, QPushButton, QVBoxLayout)

from PyQt5.QtWidgets import QWidget

from PyQt5 import QtCore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Задание 1: Кликер")
        
        Layout = QVBoxLayout()
        # Layout2 = QVBoxLayout()
        # Layout3 = QVBoxLayout()
        
    
        widget = QWidget()
        widget.setLayout(Layout)
        
        #self для использования по всему классу
        self.saveClicks = 0
        
        textLabel = QLabel(f"{self.saveClicks}")
        textLabel.setAlignment(QtCore.Qt.AlignCenter)
        Layout.addWidget(textLabel)
        
        clickerButton = QPushButton("Кликай!")
        clickerButton.clicked.connect(self.Click)
        Layout.addWidget(clickerButton)
        
        
        self.setCentralWidget(widget)
         # Button = QPushButton("Name")
         # Button.clicked.connect(self.Click)
         # self.findChild(QLineEdit).setText(str(result))
    
    def Click(self):
        self.saveClicks = self.saveClicks + 1
        
        label = self.findChild(QLabel).setText(str(self.saveClicks))
        

app=QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
