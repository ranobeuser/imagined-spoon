class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def say(self):
        print("Я - абстрактный класс, я не говорю")

class Mouse(Animal):
    def __init__(self, name, age ):
        super().__init__(name, age)

    def say(self):
        print("ПИ-ПИ-ПИ")
    
class Rat(Animal):
    def __init__(self, name, age ):
        super().__init__(name, age)
        
    def say(self):
        print("ПЬЕ-ПЬЕ_ПЬЕЕЕЕЕ")

class BreedAnimal(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed
        
    def say(self):
        print("Я - абстрактный класс, я не говорю")
        
class Cat(BreedAnimal):
    def __init__(self, name, age, breed):
        super().__init__(name, age, breed)
        
    def say(self):
        print("МММММЯЯЯЯЯЯЯЯЯЯЯУУ")
        
class Dog(BreedAnimal):
    def __init__(self, name, age, breed):
        super().__init__(name, age, breed)
        
    def say(self):
        print("ГАВ ГАВ ГАВ ГАВ ГАВ")
        
class Queue:
    def __init__(self):
        self.queue = []
    
    def add_in_queue(self, animal):
        self.queue.append(animal)
        
        print("ГАВ ГАВ ГАВ ГАВ ГАВ")
        
class Queue:
    def delete_from_queue(self):
        self.queue.remove[0]
    
    def show_first(self):
        self.queue[0].say()
        
class AnimalQueue(Queue):
    def __init__(self):
        super().__init__()
    
    def add_in_queue(self, animal):
        if isinstance(animal, BreedAnimal):
            self.queue.append(animal)
            print(f"{animal.name} успешно принят в очередь")
        else: print("Мы таких не принимаем")

sobaka = Dog("Тузик", 2, "Йорк")
mishka = Mouse("сосиска",3)

queue1 = AnimalQueue()

queue1.add_in_queue(sobaka)
queue1.add_in_queue(mishka)