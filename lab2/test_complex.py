"""
Тестовая программа 5: Комплексный пример со всеми аспектами
Демонстрирует все метрики одновременно
"""

class Vehicle:
    """Базовый класс транспортного средства"""
    
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.speed = 0
    
    def start(self):
        """Запускает транспортное средство"""
        self.speed = 10
        return "Started"
    
    def stop(self):
        """Останавливает транспортное средство"""
        self.speed = 0
        return "Stopped"
    
    def get_info(self):
        """Возвращает информацию"""
        return f"{self.brand} {self.model}"


class Car(Vehicle):
    """Класс автомобиля"""
    
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)
        self.doors = doors
        self.engine = None
    
    def set_engine(self, engine):
        """Устанавливает двигатель"""
        self.engine = engine
    
    def accelerate(self):
        """Ускоряется"""
        if self.engine:
            self.speed += self.engine.get_power()
        else:
            self.speed += 10
        return self.speed
    
    def get_doors(self):
        """Возвращает количество дверей"""
        return self.doors


class Motorcycle(Vehicle):
    """Класс мотоцикла"""
    
    def __init__(self, brand, model):
        super().__init__(brand, model)
        self.wheels = 2
    
    def wheelie(self):
        """Выполняет вилли"""
        return "Wheelie!"
    
    def get_wheels(self):
        """Возвращает количество колес"""
        return self.wheels


class Engine:
    """Класс двигателя"""
    
    def __init__(self, power):
        self.power = power
        self.running = False
    
    def start(self):
        """Запускает двигатель"""
        self.running = True
        return "Engine started"
    
    def stop(self):
        """Останавливает двигатель"""
        self.running = False
        return "Engine stopped"
    
    def get_power(self):
        """Возвращает мощность"""
        return self.power


class SportsCar(Car):
    """Спортивный автомобиль"""
    
    def __init__(self, brand, model, doors, max_speed):
        super().__init__(brand, model, doors)
        self.max_speed = max_speed
        self.turbo = False
    
    def enable_turbo(self):
        """Включает турбо"""
        self.turbo = True
        if self.engine:
            return self.engine.get_power() * 1.5
        return 0
    
    def race(self):
        """Гонка"""
        self.enable_turbo()
        return self.accelerate()

