"""
Тестовая программа 1: Простой класс без наследования
Ожидаемые метрики:
- WMC: количество методов (3)
- DIT: 0 (нет наследования)
- NOC: 0 (нет потомков)
- CBO: 0 (нет связей с другими классами)
- RFC: количество методов + вызываемые методы
- LCOM: зависит от использования атрибутов
"""

class SimpleClass:
    """Простой класс для тестирования базовых метрик"""
    
    def __init__(self, value):
        self.value = value
        self.count = 0
    
    def increment(self):
        """Увеличивает счетчик"""
        self.count += 1
        return self.count
    
    def get_value(self):
        """Возвращает значение"""
        return self.value
    
    def process(self):
        """Обрабатывает данные"""
        result = self.get_value()
        self.increment()
        return result * 2

