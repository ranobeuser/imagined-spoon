with open('pr4/gnezdilik.txt', 'r', encoding='utf-8') as file:
    # Читаем строки и сохраняем их в список
    data = file.readlines()

# Выводим информацию из списка в консоль
for i in data:
    print(i.strip())
