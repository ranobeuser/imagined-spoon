import sys
import json

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget, QTableWidgetItem, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,QStackedLayout,QLineEdit)

from PyQt5.QtGui import QColor, QPalette

from PyQt5 import QtCore

class Weather:
    def __init__(self,city,temperature,unit):
        self.city = city
        self.temperature = temperature
        self.unit = unit
    
    def show(self):
        print(f"{self.city}: {self.temperature} {self.unit}")
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Задание 3: кусок погоды в городах")
        
        self.Layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(self.Layout)
        
        #data
        with open("pr3/data.json","r", encoding='utf-8') as file:
            self.data = json.load(file)
        
        self.town_list = []
        
        k=0
        for i in self.data:
            city = i["city"]
            temperature = i["temperature"]
            unit = i["unit"]
            self.town_list.append(Weather(city, temperature, unit)) 

            self.town_list[k].show()
            k+=1
            
            
        #widgets
        self.table = QTableWidget(len(self.town_list),3)
        self.Layout.addWidget(self.table)
        
        self.table.setHorizontalHeaderLabels(["Город","Температура","Ед.изм"])
        
        for row, record in enumerate(self.town_list):
            self.table.setItem(row,0, QTableWidgetItem(record.city))
            self.table.setItem(row,1, QTableWidgetItem(str(record.temperature)))
            self.table.setItem(row,2, QTableWidgetItem(record.unit))
        
        self.setCentralWidget(widget)
         # Button = QPushButton("Name")
         # Button.clicked.connect(self.Click)
         # self.findChild(QLineEdit).setText(str(result))
    
    def Click(self):
        button = self.sender()
        text = button.text()
        
app=QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
