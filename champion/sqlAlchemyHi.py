from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Создание двигателя подключения
engine = create_engine('postgresql://student:student@localhost:5432/postgres')  # Измените на нужный вам формат

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Выполнение запроса
result = session.execute('SELECT * FROM your_table_name')

# Обработка результатов
for row in result:
    print(row)

# Закрытие сессии
session.close()
