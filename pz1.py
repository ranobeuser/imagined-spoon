import random as rd
from enum import Enum

class Degrees(Enum):
    Celsius, Fahrenheit, Kelvin = "C", "F", "K"

class Town:
    def __init__(self,name,degrees, system):
        self.name, self.degrees, self.system = name, degrees, system
    
    def ReturnNormalView(self):
        return f"Город: {self.name}, Градусы:{self.degrees}, Система: {self.system.value}"

def RoundThing(thing):
    return round(thing, ndigits=1)

def SortThing(towns):
    i = input("Введите способ сортировки:\n+ = По возрастанию\n- = По убыванию\n")
    if i=="+":
        towns.sort(key = lambda x: x.degrees)
        print(list(map(lambda x: x.ReturnNormalView(), towns)))
    elif i=="-": 
        towns.sort(key = lambda x: x.degrees, reverse=True)
        print(list(map(lambda x: x.ReturnNormalView(), towns)))
    else: print("нельзя так")

def FilterThing(towns):
    i = input("Введите способ фильтрации:\n+ = Города с температурой больше нуля или ноль\n- = Города с температурой меньше нуля\n")
    if i=="+":
        print(list(map(lambda x: x.ReturnNormalView(), list(filter(lambda x: x.degrees>=0,towns)))))
    elif i=="-": 
        print(list(map(lambda x: x.ReturnNormalView(), list(filter(lambda x: x.degrees<0,towns)))))
    else: print("нельзя так")

def ReturnThreeSystems(Object, degreesEnum):
    return [[Object.degrees, degreesEnum[0].value], [RoundThing(Object.degrees * 9/5 + 32), degreesEnum[1].value], [RoundThing(Object.degrees + 273.15), degreesEnum[2].value]]
 
towns = ["Abakan", "Sorsk", "Ust-Abakan", "Tashtip", "Bograd", "Kopievo","Abaza", "Chernogorsk"]
degrees = []
townss = []
degreesEnum = list(Degrees)
for i in range(8):
    degrees.append(rd.randint(-60,50))
    townss.append(Town(towns[i],degrees[i], Degrees.Celsius))

townName = input("Введите название города для которого хотите посмотреть градусы в трех системах:")
print(  ReturnThreeSystems(list(filter(lambda x: x.name == townName, townss))[0], degreesEnum)  )
FilterThing(townss)
SortThing(townss)




































# class SemesterResult:
#     def __init__(self, semester, student, subjects, certifications):
#         self.semester, self.student, self.subjects, self.certifications = semester, student, subjects, certifications

#     def return_session(self):
#        print(f"Семестр: {self.semester}, студент: {self.student}, предметы: {self.subjects}, зачеты: {self.certifications}")

# #Пусть оценка "хорошо" - это когда и по математике и по русскому и по истории стоит зачет

# subjectss = ["русский", "математика", "история"]
# zachet = [1,1,1]
# nezachet = [0,0,0]
# results = [SemesterResult(1,"Данил",subjectss,zachet), SemesterResult(1,"Артем", subjectss, zachet),SemesterResult(1,"Давид",subjectss,nezachet)]

# print("Сессии с количеством экзаменов >= 2:")
# new = filter(lambda i: len(i.subjecs>=2), results)
# print(new)

# print("\nСессии с количеством зачетов от 1 до 3:")
# results = filter(lambda i: len(i.certifications) in [1,2,3], results)

# print(results)