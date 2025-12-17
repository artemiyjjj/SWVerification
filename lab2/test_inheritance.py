"""
Тестовая программа 2: Иерархия наследования
Ожидаемые метрики:
- BaseClass: DIT=0, NOC=2 (Child1, Child2)
- Child1: DIT=1, NOC=1 (GrandChild)
- Child2: DIT=1, NOC=0
- GrandChild: DIT=2, NOC=0
"""

class BaseClass:
    """Базовый класс"""
    
    def __init__(self):
        self.base_attr = "base"
    
    def base_method(self):
        """Базовый метод"""
        return self.base_attr
    
    def common_method(self):
        """Общий метод"""
        return "common"


class Child1(BaseClass):
    """Первый потомок BaseClass"""
    
    def __init__(self):
        super().__init__()
        self.child1_attr = "child1"
    
    def child1_method(self):
        """Метод первого потомка"""
        return self.child1_attr
    
    def common_method(self):
        """Переопределенный метод"""
        return "child1_common"


class Child2(BaseClass):
    """Второй потомок BaseClass"""
    
    def __init__(self):
        super().__init__()
        self.child2_attr = "child2"
    
    def child2_method(self):
        """Метод второго потомка"""
        return self.child2_attr


class GrandChild(Child1):
    """Потомок Child1"""
    
    def __init__(self):
        super().__init__()
        self.grandchild_attr = "grandchild"
    
    def grandchild_method(self):
        """Метод внука"""
        return self.grandchild_attr

