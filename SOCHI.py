class Vehicle:
    def __init__(self, make, model, year):
        self.make, self.model, self.year, self.speed = make, model, year, 0
    
    def accelerate(self,x):
        self.speed+=x
    
    def brake(self,x):
        self.speed-=x
        if self.speed<0: self.speed=0
    
    def get_into(self):
        print(f"Производитель: {make}\nМодель: {model}\nГод выпуска: {year}\nТекущая скорость: {speed}")
    
class Car(Vehicle):
    def __init__(self, make, model, year, fuel_type):
        super().__init__(make,model,year)
        self.fuel_type = fuel_type
    
    def refuel(self):
        print("бибика заправлена")
        
class Bicycle(Vehicle):
    def __init__(self, make, model, year, gear_count):
        super().__init__(make,model,year)
        self.gear_count = gear_count
        self.gear = 0
    
    def change_gear(self, new_gear):
        self.gear = new_gear
        
class Motorcycle(Vehicle):
    def __init__(self, make, model, year, max_speed):
        super().__init__(make,model,year)
        self.max_speed = max_speed
    
    def just_break(self):
        print("ВЫ СЛОМАЛИ МОТОЦИКЛ")
        
a = Car("мужики","XXX22132", "2024","бензин")

a.refuel()

b = Bicycle("мужики","XXX22132", "2024", 5)

b.change_gear(5)