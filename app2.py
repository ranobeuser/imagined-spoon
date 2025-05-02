import sys
import psycopg2
from datetime import date
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QLineEdit, QHeaderView, QAbstractItemView, QMessageBox)
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Модели БД
class Passport(Base):
    __tablename__ = 'passports'
    passport_id = Column(Integer, primary_key=True)
    seria = Column(String(11))
    number = Column(String(11))
    birth_place = Column(String)
    issuance_place = Column(String)
    issuance_date = Column(Date)
    permanent_address = Column(String)

class Guest(Base):
    __tablename__ = 'guests'
    guest_id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    fathername = Column(String)
    phone = Column(String)
    date_of_birth = Column(Date)
    passport_id = Column(Integer, ForeignKey('passports.passport_id'))
    passport = relationship("Passport")

class ServiceType(Base):
    __tablename__ = 'service_types'
    service_type_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(30))
    price_per_hour = Column(Integer)

class Service(Base):
    __tablename__ = 'services'
    service_id = Column(Integer, primary_key=True)
    service_date = Column(Date)
    hours_amount = Column(Integer)
    service_type_id = Column(Integer, ForeignKey('service_types.service_type_id'))
    service_type = relationship("ServiceType")

class RoomType(Base):
    __tablename__ = 'room_types'
    room_type_id = Column(Integer, primary_key=True)
    name = Column(String)
    equipment = Column(String)
    description = Column(String)
    price_per_day = Column(Integer)

class Room(Base):
    __tablename__ = 'rooms'
    room_id = Column(Integer, primary_key=True)
    room_number = Column(Integer)
    room_type_id = Column(Integer, ForeignKey('room_types.room_type_id'))
    room_type = relationship("RoomType")

class Reservation(Base):
    __tablename__ = 'reservations'
    reservation_id = Column(Integer, primary_key=True)
    enter_date = Column(Date)
    exit_date = Column(Date)
    price = Column(Integer)
    room_id = Column(Integer, ForeignKey('rooms.room_id'))
    room = relationship("Room")

# Настройка подключения к БД
engine = create_engine('postgresql+psycopg2://postgres@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

class HotelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_table = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Управление гостиницей')
        self.setGeometry(100, 100, 1200, 600)
        
        main_layout = QHBoxLayout()
        
        # Левая панель с кнопками
        btn_layout = QVBoxLayout()
        self.btn_guests = QPushButton('Клиенты')
        self.btn_rooms = QPushButton('Номерной фонд')
        self.btn_services = QPushButton('Доп. услуги')
        self.btn_reservations = QPushButton('Бронирования')
        
        for btn in [self.btn_guests, self.btn_rooms, self.btn_services, self.btn_reservations]:
            btn.setFixedHeight(40)
            btn.setStyleSheet("QPushButton {font-size: 14pt;}")
            
        btn_layout.addWidget(self.btn_guests)
        btn_layout.addWidget(self.btn_rooms)
        btn_layout.addWidget(self.btn_services)
        btn_layout.addWidget(self.btn_reservations)
        btn_layout.addStretch()
        
        # Правая панель с таблицей и поиском
        right_panel = QVBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.table.cellChanged.connect(self.save_changes)
        
        right_panel.addWidget(self.search_input)
        right_panel.addWidget(self.table)
        
        main_layout.addLayout(btn_layout, 1)
        main_layout.addLayout(right_panel, 4)
        self.setLayout(main_layout)
        
        # Подключение сигналов
        self.btn_guests.clicked.connect(lambda: self.load_data('guests'))
        self.btn_rooms.clicked.connect(lambda: self.load_data('rooms'))
        self.btn_services.clicked.connect(lambda: self.load_data('services'))
        self.btn_reservations.clicked.connect(lambda: self.load_data('reservations'))
        self.search_input.textChanged.connect(self.apply_filter)

    def load_data(self, table_name):
        self.current_table = table_name
        self.table.clear()
        
        if table_name == 'guests':
            query = session.query(Guest).join(Passport)
            headers = ['ID', 'Фамилия', 'Имя', 'Отчество', 'Телефон', 'Дата рождения', 
                      'Паспорт серия', 'Паспорт номер', 'Дата выдачи паспорта']
            
        elif table_name == 'rooms':
            query = session.query(Room).join(RoomType)
            headers = ['ID', 'Номер', 'Тип номера', 'Оборудование', 'Цена за день']
            
        elif table_name == 'services':
            query = session.query(Service).join(ServiceType)
            headers = ['ID', 'Дата услуги', 'Кол-во часов', 'Тип услуги', 'Цена за час', 'Стоимость']
            
        elif table_name == 'reservations':
            query = session.query(Reservation).join(Room)
            headers = ['ID', 'Дата заезда', 'Дата выезда', 'Стоимость', 'Номер комнаты']
            
        data = query.all()
        
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        for row_idx, item in enumerate(data):
            if table_name == 'guests':
                self.fill_guest_row(row_idx, item)
            elif table_name == 'rooms':
                self.fill_room_row(row_idx, item)
            elif table_name == 'services':
                self.fill_service_row(row_idx, item)
            elif table_name == 'reservations':
                self.fill_reservation_row(row_idx, item)

    def fill_guest_row(self, row_idx, guest):
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(guest.guest_id)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(guest.surname))
        self.table.setItem(row_idx, 2, QTableWidgetItem(guest.name))
        self.table.setItem(row_idx, 3, QTableWidgetItem(guest.fathername))
        self.table.setItem(row_idx, 4, QTableWidgetItem(guest.phone))
        self.table.setItem(row_idx, 5, QTableWidgetItem(str(guest.date_of_birth)))
        if guest.passport:
            self.table.setItem(row_idx, 6, QTableWidgetItem(guest.passport.seria))
            self.table.setItem(row_idx, 7, QTableWidgetItem(guest.passport.number))
            self.table.setItem(row_idx, 8, QTableWidgetItem(str(guest.passport.issuance_date)))

    def fill_room_row(self, row_idx, room):
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(room.room_id)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(str(room.room_number)))
        if room.room_type:
            self.table.setItem(row_idx, 2, QTableWidgetItem(room.room_type.name))
            self.table.setItem(row_idx, 3, QTableWidgetItem(room.room_type.equipment))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(room.room_type.price_per_day)))

    def fill_service_row(self, row_idx, service):
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(service.service_id)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(str(service.service_date)))
        self.table.setItem(row_idx, 2, QTableWidgetItem(str(service.hours_amount)))
        if service.service_type:
            self.table.setItem(row_idx, 3, QTableWidgetItem(service.service_type.name))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(service.service_type.price_per_hour)))
            total = service.hours_amount * service.service_type.price_per_hour
            self.table.setItem(row_idx, 5, QTableWidgetItem(str(total)))

    def fill_reservation_row(self, row_idx, reservation):
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(reservation.reservation_id)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(str(reservation.enter_date)))
        self.table.setItem(row_idx, 2, QTableWidgetItem(str(reservation.exit_date)))
        self.table.setItem(row_idx, 3, QTableWidgetItem(str(reservation.price)))
        if reservation.room:
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(reservation.room.room_number)))

    def save_changes(self, row, column):
        try:
            if self.current_table == 'guests':
                guest_id = int(self.table.item(row, 0).text())
                guest = session.query(Guest).get(guest_id)
                
                if column == 1: guest.surname = self.table.item(row, column).text()
                elif column == 2: guest.name = self.table.item(row, column).text()
                elif column == 3: guest.fathername = self.table.item(row, column).text()
                elif column == 4: guest.phone = self.table.item(row, column).text()
                
                session.commit()
                
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка сохранения: {str(e)}')
            session.rollback()

    def apply_filter(self, text):
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and text.lower() in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HotelApp()
    window.show()
    
    sys.exit(app.exec_())