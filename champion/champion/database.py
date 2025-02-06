from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Создание двигателя подключения
engine = create_engine('postgresql://postgres:student@localhost:5432/paymentdb', echo = True)  # Измените на нужный вам формат

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Выполнение запроса
result = session.execute('SELECT * FROM payment')

# Обработка результатов
for row in result:
    print(row[3])

# Закрытие сессии
session.close()
