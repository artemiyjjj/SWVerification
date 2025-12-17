"""
Тестовая программа 4: Тестирование связности методов (Cohesion)
Ожидаемые метрики:
- HighCohesionClass: низкий LCOM (методы используют общие атрибуты)
- LowCohesionClass: высокий LCOM (методы не используют общие атрибуты)
"""

class HighCohesionClass:
    """Класс с высокой связностью методов"""
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.result = 0
    
    def set_x(self, value):
        self.x = value
        self.update_result()
    
    def set_y(self, value):
        self.y = value
        self.update_result()
    
    def update_result(self):
        self.result = self.x + self.y
    
    def get_result(self):
        return self.result
    
    def calculate(self):
        return self.x * self.y + self.result


class LowCohesionClass:
    """Класс с низкой связностью методов"""
    
    def __init__(self):
        self.attr1 = "attr1"
        self.attr2 = 100
        self.attr3 = [1, 2, 3]
    
    def method1(self):
        return self.attr1.upper()
    
    def method2(self):
        return self.attr2 * 2
    
    def method3(self):
        return sum(self.attr3)
    
    def method4(self):
        return "constant"
    
    def method5(self):
        return 42

