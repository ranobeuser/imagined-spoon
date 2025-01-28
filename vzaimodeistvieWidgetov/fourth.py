import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QMessageBox, QApplication)

from PyQt5 import QtCore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 4: Данные в лейбле, без кнопки подтвердить")
        self.setGeometry(100,100,400,150)
        
        self.Layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(self.Layout)
        
        self.fio, self.town, self.sex = "", "", ""
        
        self.text2_label = QLabel("Введите в строку снизу свое ФИО \nЗатем выберите свой город и пол из выпадающих списков и ждите чуда")
        self.text2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Layout.addWidget(self.text2_label)
        
        self.line_edit  = QLineEdit(self)
        self.line_edit.textChanged.connect(self.Replace)
        self.Layout.addWidget(self.line_edit)
        
        self.town_combo = QComboBox()
        self.town_combo.addItems(["Черногорск","Абакан"])
        self.town_combo.currentTextChanged.connect(self.Replace)
        self.Layout.addWidget(self.town_combo)
        
        self.sex_combo = QComboBox()
        self.sex_combo.addItems(["Мужчина","Женщина","Вертолет"])
        self.sex_combo.currentTextChanged.connect(self.Replace)
        self.Layout.addWidget(self.sex_combo)
        
        self.text_variable = f"Ваша информация:\nФИО: {self.fio}\nГород: {self.town}\nПол: {self.sex}"
    
        self.text_label = QLabel(self.text_variable)
        self.text_label.setAlignment(QtCore.Qt.AlignTop)
        self.Layout.addWidget(self.text_label)
        
        self.setCentralWidget(widget)
         # Button = QPushButton("Name")
         # Button.clicked.connect(self.Click)
         # self.findChild(QLineEdit).setText(str(result))
    
    def Replace(self):
        self.text_label.setText(f"Ваша информация:\nФИО: {self.line_edit.text()}\nГород: {self.town_combo.currentText()}\nПол: {self.sex_combo.currentText()}")


app=QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()