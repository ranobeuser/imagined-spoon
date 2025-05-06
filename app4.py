import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTableView, QSplitter, QPushButton,
                             QVBoxLayout, QHBoxLayout, QDialog, QLineEdit, QComboBox, QFormLayout,
                             QMessageBox, QLabel, QDateEdit, QScrollArea, QGroupBox, QRadioButton)
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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

# Модель для отображения данных в таблице
class TableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return QVariant()

# Диалог добавления записей
class AddDialog(QDialog):
    def __init__(self, table_name, session, parent=None):
        super().__init__(parent)
        self.table_name = table_name
        self.session = session
        self.setup_ui()
        self.setMinimumWidth(400)
        
    def setup_ui(self):
        self.setWindowTitle(f"Добавить в {self.table_name}")
        layout = QFormLayout()
        
        self.fields = {}
        date_edit = lambda: QDateEdit(calendarPopup=True)
        number_edit = lambda: QLineEdit()
        
        if self.table_name == 'guests':
            self.fields['surname'] = QLineEdit()
            self.fields['name'] = QLineEdit()
            self.fields['fathername'] = QLineEdit()
            self.fields['phone'] = QLineEdit()
            self.fields['date_of_birth'] = date_edit()
            
            self.fields['passport'] = QComboBox()
            passports = self.session.query(Passport).all()
            for p in passports:
                self.fields['passport'].addItem(f"{p.seria} {p.number}", p.passport_id)

            layout.addRow("Фамилия:", self.fields['surname'])
            layout.addRow("Имя:", self.fields['name'])
            layout.addRow("Отчество:", self.fields['fathername'])
            layout.addRow("Телефон:", self.fields['phone'])
            layout.addRow("Дата рождения:", self.fields['date_of_birth'])
            layout.addRow("Паспорт:", self.fields['passport'])

        elif self.table_name == 'rooms':
            self.fields['room_number'] = number_edit()
            
            self.fields['room_type'] = QComboBox()
            room_types = self.session.query(RoomType).all()
            for rt in room_types:
                self.fields['room_type'].addItem(rt.name, rt.room_type_id)

            layout.addRow("Номер комнаты:", self.fields['room_number'])
            layout.addRow("Тип номера:", self.fields['room_type'])

        elif self.table_name == 'services':
            self.fields['service_date'] = date_edit()
            self.fields['hours_amount'] = number_edit()
            
            self.fields['service_type'] = QComboBox()
            service_types = self.session.query(ServiceType).all()
            for st in service_types:
                self.fields['service_type'].addItem(st.name, st.service_type_id)

            layout.addRow("Дата услуги:", self.fields['service_date'])
            layout.addRow("Количество часов:", self.fields['hours_amount'])
            layout.addRow("Тип услуги:", self.fields['service_type'])

        elif self.table_name == 'reservations':
            self.fields['enter_date'] = date_edit()
            self.fields['exit_date'] = date_edit()
            self.fields['price'] = number_edit()
            
            self.fields['room'] = QComboBox()
            rooms = self.session.query(Room).all()
            for r in rooms:
                self.fields['room'].addItem(f"№{r.room_number}", r.room_id)

            layout.addRow("Дата заезда:", self.fields['enter_date'])
            layout.addRow("Дата выезда:", self.fields['exit_date'])
            layout.addRow("Стоимость:", self.fields['price'])
            layout.addRow("Номер:", self.fields['room'])

        elif self.table_name == 'service_types':
            self.fields['name'] = QLineEdit()
            self.fields['description'] = QLineEdit()
            self.fields['price_per_hour'] = number_edit()

            layout.addRow("Название:", self.fields['name'])
            layout.addRow("Описание:", self.fields['description'])
            layout.addRow("Цена за час:", self.fields['price_per_hour'])

        elif self.table_name == 'room_types':
            self.fields['name'] = QLineEdit()
            self.fields['equipment'] = QLineEdit()
            self.fields['description'] = QLineEdit()
            self.fields['price_per_day'] = number_edit()

            layout.addRow("Название:", self.fields['name'])
            layout.addRow("Оборудование:", self.fields['equipment'])
            layout.addRow("Описание:", self.fields['description'])
            layout.addRow("Цена за день:", self.fields['price_per_day'])

        elif self.table_name == 'passports':
            self.fields['seria'] = QLineEdit()
            self.fields['number'] = QLineEdit()
            self.fields['birth_place'] = QLineEdit()
            self.fields['issuance_place'] = QLineEdit()
            self.fields['issuance_date'] = date_edit()
            self.fields['permanent_address'] = QLineEdit()

            layout.addRow("Серия:", self.fields['seria'])
            layout.addRow("Номер:", self.fields['number'])
            layout.addRow("Место рождения:", self.fields['birth_place'])
            layout.addRow("Место выдачи:", self.fields['issuance_place'])
            layout.addRow("Дата выдачи:", self.fields['issuance_date'])
            layout.addRow("Адрес:", self.fields['permanent_address'])

        btn_submit = QPushButton("Добавить")
        btn_submit.clicked.connect(self.submit)
        layout.addRow(btn_submit)
        self.setLayout(layout)

    def submit(self):
        try:
            if self.table_name == 'guests':
                guest = Guest(
                    surname=self.fields['surname'].text(),
                    name=self.fields['name'].text(),
                    fathername=self.fields['fathername'].text(),
                    phone=self.fields['phone'].text(),
                    date_of_birth=self.fields['date_of_birth'].date().toPyDate(),
                    passport_id=self.fields['passport'].currentData()
                )
                self.session.add(guest)

            elif self.table_name == 'rooms':
                room = Room(
                    room_number=int(self.fields['room_number'].text()),
                    room_type_id=self.fields['room_type'].currentData()
                )
                self.session.add(room)

            elif self.table_name == 'services':
                service = Service(
                    service_date=self.fields['service_date'].date().toPyDate(),
                    hours_amount=int(self.fields['hours_amount'].text()),
                    service_type_id=self.fields['service_type'].currentData()
                )
                self.session.add(service)

            elif self.table_name == 'reservations':
                reservation = Reservation(
                    enter_date=self.fields['enter_date'].date().toPyDate(),
                    exit_date=self.fields['exit_date'].date().toPyDate(),
                    price=int(self.fields['price'].text()),
                    room_id=self.fields['room'].currentData()
                )
                self.session.add(reservation)

            elif self.table_name == 'service_types':
                service_type = ServiceType(
                    name=self.fields['name'].text(),
                    description=self.fields['description'].text(),
                    price_per_hour=int(self.fields['price_per_hour'].text())
                )
                self.session.add(service_type)

            elif self.table_name == 'room_types':
                room_type = RoomType(
                    name=self.fields['name'].text(),
                    equipment=self.fields['equipment'].text(),
                    description=self.fields['description'].text(),
                    price_per_day=int(self.fields['price_per_day'].text())
                )
                self.session.add(room_type)

            elif self.table_name == 'passports':
                passport = Passport(
                    seria=self.fields['seria'].text(),
                    number=self.fields['number'].text(),
                    birth_place=self.fields['birth_place'].text(),
                    issuance_place=self.fields['issuance_place'].text(),
                    issuance_date=self.fields['issuance_date'].date().toPyDate(),
                    permanent_address=self.fields['permanent_address'].text()
                )
                self.session.add(passport)

            self.session.commit()
            self.accept()
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка ввода", "Проверьте правильность числовых значений")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            self.session.rollback()

# Окно графиков
class ChartsWindow(QDialog):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Аналитика")
        layout = QVBoxLayout()

        # Выбор типа графика
        self.chart_type = QComboBox()
        self.chart_type.addItems(["Гистограмма", "Линейный", "Круговая"])
        
        # Контейнер для графиков
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        layout.addWidget(self.chart_type)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        self.chart_type.currentIndexChanged.connect(self.update_charts)
        self.update_charts()

    def update_charts(self):
        self.figure.clear()
        
        # График 1: Заселяемость
        ax1 = self.figure.add_subplot(121)
        reservations = self.session.query(Reservation).all()
        dates = [res.enter_date for res in reservations]
        date_counts = {}
        for date in dates:
            date_str = date.strftime("%Y-%m-%d")
            date_counts[date_str] = date_counts.get(date_str, 0) + 1
        
        # График 2: Доход по типам номеров
        ax2 = self.figure.add_subplot(122)
        room_types = self.session.query(RoomType).all()
        prices = [rt.price_per_day for rt in room_types]
        labels = [rt.name for rt in room_types]

        chart_type = self.chart_type.currentText()
        self.plot_chart(ax1, list(date_counts.keys()), list(date_counts.values()), chart_type, "Заселяемость")
        self.plot_chart(ax2, labels, prices, chart_type, "Доход по типам номеров")

        self.canvas.draw()

    def plot_chart(self, ax, x, y, chart_type, title):
        ax.clear()
        if chart_type == "Гистограмма":
            ax.bar(x, y)
        elif chart_type == "Линейный":
            ax.plot(x, y)
        elif chart_type == "Круговая":
            ax.pie(y, labels=x, autopct='%1.1f%%')
        ax.set_title(title)

# Основное окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.current_table = None

    def setup_ui(self):
        self.setWindowTitle("Управление гостиницей")
        self.setGeometry(100, 100, 1200, 800)

        splitter = QSplitter(Qt.Horizontal)
        
        # Левая панель
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        tables = ['guests', 'rooms', 'services', 'reservations']
        for table in tables:
            btn = QPushButton(table.capitalize())
            btn.clicked.connect(lambda _, t=table: self.load_table(t))
            
            left_layout.addWidget(btn)
        
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_record)
        left_layout.addWidget(self.btn_add)
        
        self.btn_charts = QPushButton("Графики")
        self.btn_charts.clicked.connect(self.show_charts)
        left_layout.addWidget(self.btn_charts)
        
        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        
        # Правая панель
        self.table_view = QTableView()
        
        splitter.addWidget(left_panel)
        splitter.addWidget(self.table_view)
        self.setCentralWidget(splitter)

    def load_table(self, table_name):
        self.current_table = table_name
        data, headers = [], []
        
        if table_name == 'guests':
            guests = session.query(Guest).options(joinedload(Guest.passport)).all()
            headers = ['ID', 'Фамилия', 'Имя', 'Отчество', 'Телефон', 'Дата рождения', 'Паспорт']
            data = [
                [g.guest_id, g.surname, g.name, g.fathername, g.phone, 
                 g.date_of_birth.strftime("%Y-%m-%d"), 
                 f"{g.passport.seria} {g.passport.number}" if g.passport else ""]
                for g in guests
            ]

        if table_name == 'rooms':
            rooms = session.query(Room).options(joinedload(Room.room_type)).all()
            headers = ['ID', 'Номер', 'Тип номера', 'Цена за день', 'Оборудование', 'Описание']
            data = [
                [r.room_id, r.room_number,
                 r.room_type.name if r.room_type else "",
                 r.room_type.price_per_day if r.room_type else "",
                 r.room_type.equipment if r.room_type else "",
                 r.room_type.description if r.room_type else ""]
                for r in rooms
            ]
        elif table_name == 'services':
            services = session.query(Service).options(joinedload(Service.service_type)).all()
            headers = ['ID', 'Дата', 'Часы', 'Тип услуги', 'Стоимость']
            data = [
                [s.service_id, s.service_date.strftime("%Y-%m-%d"), 
                s.hours_amount,
                s.service_type.name if s.service_type else "",
                (s.service_type.price_per_hour * s.hours_amount) if s.service_type else 0]
                for s in services
            ]

        elif table_name == 'reservations':
            reservations = session.query(Reservation).options(joinedload(Reservation.room)).all()
            headers = ['ID', 'Заезд', 'Выезд', 'Стоимость', 'Номер', 'Тип номера']
            data = [
                [r.reservation_id, 
                r.enter_date.strftime("%Y-%m-%d"),
                r.exit_date.strftime("%Y-%m-%d"),
                r.price,
                r.room.room_number if r.room else "",
                r.room.room_type.name if r.room and r.room.room_type else ""]
                for r in reservations
            ]
        
        # Аналогичные запросы для других таблиц...
        
        model = TableModel(data, headers)
        self.table_view.setModel(model)

    def add_record(self):
        if self.current_table:
            dialog = AddDialog(self.current_table, session, self)
            if dialog.exec_() == QDialog.Accepted:
                self.load_table(self.current_table)

    def show_charts(self):
        dialog = ChartsWindow(session)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Раскомментировать для заполнения тестовыми данными

    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())