"""
Тестовая программа 3: Связность между классами (Coupling)
Ожидаемые метрики:
- ClassA: CBO должен учитывать использование ClassB и ClassC
- ClassB: CBO должен учитывать использование ClassA
- ClassC: CBO должен учитывать использование ClassA
"""

class ClassA:
    """Класс A, использующий другие классы"""
    
    def __init__(self):
        self.value = 10
        self.class_b = None
        self.class_c = None
    
    def set_class_b(self, b):
        """Устанавливает связь с ClassB"""
        self.class_b = b
    
    def set_class_c(self, c):
        """Устанавливает связь с ClassC"""
        self.class_c = c
    
    def process_with_b(self):
        """Использует ClassB"""
        if self.class_b:
            return self.class_b.get_data()
        return None
    
    def process_with_c(self):
        """Использует ClassC"""
        if self.class_c:
            return self.class_c.compute()
        return None


class ClassB:
    """Класс B, использующий ClassA"""
    
    def __init__(self):
        self.data = "data from B"
        self.class_a = None
    
    def set_class_a(self, a):
        """Устанавливает связь с ClassA"""
        self.class_a = a
    
    def get_data(self):
        """Возвращает данные"""
        return self.data
    
    def use_class_a(self):
        """Использует ClassA"""
        if self.class_a:
            return self.class_a.value
        return None


class ClassC:
    """Класс C, использующий ClassA"""
    
    def __init__(self):
        self.factor = 2
        self.class_a = None
    
    def set_class_a(self, a):
        """Устанавливает связь с ClassA"""
        self.class_a = a
    
    def compute(self):
        """Вычисляет значение"""
        if self.class_a:
            return self.class_a.value * self.factor
        return 0

