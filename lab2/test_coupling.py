"""
Тестовая программа 3: Связность между классами (Coupling)
Ожидаемые метрики:
- ClassA: CBO должен учитывать использование ClassB и ClassC
- ClassB: CBO должен учитывать использование Class C
"""

class ClassC:
    """Класс C, использующий ClassA"""
    
    def __init__(self):
        self.factor = 2

    def get_factor(self):
        return self.factor
    

class ClassB:
    """Класс B, использующий ClassA"""
    
    def __init__(self):
        self.data = "data from B"
        self.class_c : ClassC = ClassC()
    
    def set_class_c(self, c: ClassC):
        """Устанавливает связь с ClassA"""
        self.class_c = c
    
    def get_data(self):
        """Возвращает данные"""
        return self.data
    
    def use_class_c(self):
        """Использует ClassC"""
        return self.class_c.factor

class ClassA:
    """Класс A, использующий другие классы"""
    
    def __init__(self):
        self.value = 10
        self.class_b = ClassB()
        self.class_c = ClassC()
    
    def set_class_b(self, b: ClassB):
        """Устанавливает связь с ClassB"""
        self.class_b = b
    
    def set_class_c(self, c: ClassC):
        """Устанавливает связь с ClassC"""
        self.class_c = c
    
    def process_with_b(self):
        """Использует ClassB"""
        if self.class_b:
            return self.class_b.get_data()
        return None
    
    def process_with_c(self):
        """Использует ClassC"""
        return self.class_c.get_factor()

