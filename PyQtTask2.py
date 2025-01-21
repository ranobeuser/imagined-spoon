import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QGroupBox, QRadioButton, QWidget, QMainWindow, QComboBox, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,QStackedLayout,QLineEdit,QTimeEdit,QLCDNumber)

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget

from PyQt5 import QtCore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Задание 2: изменение текста")
        
        self.Layout = QVBoxLayout()
        self.Layout1 = QVBoxLayout()
        self.Layout2 = QVBoxLayout()
        
        widget = QWidget()
        widget.setLayout(self.Layout)
        
        self.Layout.addLayout(self.Layout1)
        self.Layout.addLayout(self.Layout2)
        
        self.labelText = "Собачка! Черепашка! ТАРАКАН!"
        
        self.textLabel = QLabel(f"{self.labelText}")
        self.textLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Layout1.addWidget(self.textLabel)
        
        self.colorComboBox = QComboBox()
        self.colorComboBox.addItems(["черный", "красный", "синий"])
        self.colorComboBox.currentIndexChanged.connect(self.updateText)
        self.Layout2.addWidget(self.colorComboBox)
        
        self.bold_checkbox = QCheckBox("Жирный")
        self.bold_checkbox.stateChanged.connect(self.updateText)
        self.Layout2.addWidget(self.bold_checkbox)

        self.italic_checkbox = QCheckBox("Курсив")
        self.italic_checkbox.stateChanged.connect(self.updateText)
        self.Layout2.addWidget(self.italic_checkbox)
        
        self.size_group = QGroupBox("Размер текста")
        self.size_layout = QHBoxLayout()

        self.size_small = QRadioButton("Маленький")
        self.size_medium = QRadioButton("Средний")
        self.size_large = QRadioButton("Большой")
        
        self.size_small.toggled.connect(self.updateText)
        self.size_medium.toggled.connect(self.updateText)
        self.size_large.toggled.connect(self.updateText)
        
        self.size_layout.addWidget(self.size_small)
        self.size_layout.addWidget(self.size_medium)
        self.size_layout.addWidget(self.size_large)
        
        self.size_small.setChecked(True)
        
        self.size_group.setLayout(self.size_layout)
        self.Layout2.addWidget(self.size_group)
        
        self.setCentralWidget(widget)
        self.updateText()
         # Button = QPushButton("Name")
         # Button.clicked.connect(self.Click)
         # self.findChild(QLineEdit).setText(str(result))

    def updateText(self):
        print("hi")
        color = self.colorComboBox.currentText()

        if color == "черный":
            color = "black"
        elif color == "красный":
            color = "red"
        elif color == "синий":
            color = "blue"

        font_weight = "normal"
        if self.bold_checkbox.isChecked():
            font_weight = "bold"
        font_italic = "italic" if self.italic_checkbox.isChecked() else "normal"


        font_size = 12
        if self.size_medium.isChecked():
            font_size = 16
        elif self.size_large.isChecked():
            font_size = 20

        self.textLabel.setStyleSheet(f"color: {color}; font-weight: {font_weight}; font-style: {font_italic}; font-size: {font_size}px;")
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
