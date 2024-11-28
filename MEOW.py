from abc import ABC, abstractmethod

class AnimalStrategy(ABC): #абстрактный базовый класс всех стратегий

    @abstractmethod
    def use_strategy(self, animal, action): pass #абстрактный метод использования стратегии

class MeowStrategy(AnimalStrategy):
    def use_strategy(self, animal, speech):
        print(f"{animal.name} мяукнул: {speech}")
 
class FlyStrategy(AnimalStrategy):
    def use_strategy(self, animal, destination):
        print(f"{animal.name} полетел в {destination}")
                
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.currentStrategy = None

    def set_strategy(self, newStrategy):
        self.currentStrategy = newStrategy
    
class Cat(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)
    
    def use_strategy(self, speech):
        self.currentStrategy.use_strategy(self, speech)
        
class Bird(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)

    def use_strategy(self, destination):
        self.currentStrategy.use_strategy(self, destination)

myaukalka = Cat("Мяукалка", 10)
letalka = Bird("Леталкалка", 5)

myaukalka.set_strategy(MeowStrategy())
myaukalka.use_strategy("мяу - мяу мяу. Мяу: мяу.")

letalka.set_strategy(FlyStrategy())
letalka.use_strategy("Сан-франциско")