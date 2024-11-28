class Computer():
    def __init__(self):
        self.cpu, self.operativeMemory, self.storage, self.videocard, self.components = None, None, None, None, []
    
    def show(self):
        print(f"Компьютер:\n    CPU: {self.cpu}\n   Оперативка: {self.operativeMemory}\n    Накопитель: {self.storage}\n    Видеокарта: {self.videocard}\n     Компоненты: {self.components}")
        
class ComputerBuilder:
    def __init__(self):
        self.computer = Computer() #pc for building
    
    def set_cpu(self,cpu):
        self.computer.cpu = cpu
        return self
        
    def set_operativeMemory(self, operativeMemory):
        self.computer.operativeMemory = operativeMemory
        return self
        
    def set_storage(self, storage):
        self.computer.storage = storage
        return self
        
    def set_videocard(self, videocard):
        self.computer.videocard = videocard
        return self
        
    def set_components(self, components):
        self.computer.components = components
        return self
    
    def produce(self):
        return self.computer
    
builder = ComputerBuilder()
computer = (builder.set_cpu("DRAGONXXXWWW").set_operativeMemory("MANYGYGABYTES12311").set_storage("MANYTERRABYTES45555XX").set_videocard("RTX3060").set_components(["something","cables"]).produce())
computer.show()