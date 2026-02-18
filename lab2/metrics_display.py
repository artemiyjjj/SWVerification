"""
Модуль для отображения метрик Чидамбера и Кемерера
"""

from typing import Dict, List
from ck_metrics import ProgramModel, CKMetricsCalculator


class MetricsDisplay:
    """Класс для отображения метрик"""
    
    def __init__(self, calculator: CKMetricsCalculator):
        self.calculator = calculator
    
    def display_class_metrics(self, class_name: str):
        """Отобразить метрики для одного класса"""
        metrics = self.calculator.calculate_all_metrics(class_name)
        
        print(f"\n{'='*60}")
        print(f"Класс: {class_name}")
        print(f"{'='*60}")
        print(f"WMC (Weighted Methods per Class):     {metrics['WMC']:3d}")
        print(f"DIT (Depth of Inheritance Tree):      {metrics['DIT']:3d}")
        print(f"NOC (Number of Children):             {metrics['NOC']:3d}")
        print(f"CBO (Coupling Between Objects):       {metrics['CBO']:3d}")
        print(f"RFC (Response For a Class):           {metrics['RFC']:3d}")
        print(f"LCOM (Lack of Cohesion of Methods):   {metrics['LCOM']:3d}")
        print(f"{'='*60}")
    
    def display_all_metrics(self):
        """Отобразить метрики для всех классов"""
        print("\n" + "="*80)
        print("МЕТРИКИ ЧИДАМБЕРА И КЕМЕРЕРА (CK METRICS)")
        print("="*80)
        
        for class_name in sorted(self.calculator.model.classes.keys()):
            self.display_class_metrics(class_name)
        
        print("\n")
    
    def display_summary_table(self):
        """Отобразить сводную таблицу метрик"""
        print("="*60)
        
        # Заголовок таблицы
        header = f"{'Класс':<20} {'WMC':>5} {'DIT':>5} {'NOC':>5} {'CBO':>5} {'RFC':>5} {'LCOM':>6}"
        print(header)
        print("-" * 60)
        
        # Данные для каждого класса
        for class_name in sorted(self.calculator.model.classes.keys()):
            metrics = self.calculator.calculate_all_metrics(class_name)
            row = (f"{class_name:<20} "
                   f"{metrics['WMC']:>5} "
                   f"{metrics['DIT']:>5} "
                   f"{metrics['NOC']:>5} "
                   f"{metrics['CBO']:>5} "
                   f"{metrics['RFC']:>5} "
                   f"{metrics['LCOM']:>6}")
            print(row)
        
        # print("="*60)
        # print("\nОписание метрик:")
        # print("  WMC - Weighted Methods per Class (взвешенное количество методов)")
        # print("  DIT - Depth of Inheritance Tree (глубина дерева наследования)")
        # print("  NOC - Number of Children (количество потомков)")
        # print("  CBO - Coupling Between Objects (связность между объектами)")
        # print("  RFC - Response For a Class (ответ класса на сообщение)")
        # print("  LCOM - Lack of Cohesion of Methods (недостаток связности методов)")
        # print()
    
    def export_to_csv(self, filename: str = "ck_metrics.csv"):
        """Экспортировать метрики в CSV файл"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Заголовок
            writer.writerow(['Класс', 'WMC', 'DIT', 'NOC', 'CBO', 'RFC', 'LCOM'])
            
            # Данные
            for class_name in sorted(self.calculator.model.classes.keys()):
                metrics = self.calculator.calculate_all_metrics(class_name)
                writer.writerow([
                    class_name,
                    metrics['WMC'],
                    metrics['DIT'],
                    metrics['NOC'],
                    metrics['CBO'],
                    metrics['RFC'],
                    metrics['LCOM']
                ])
        
        print(f"Метрики экспортированы в файл: {filename}")

