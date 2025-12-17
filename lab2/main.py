"""
Главный скрипт для вычисления и отображения метрик Чидамбера и Кемерера
"""

import sys
import os
from ck_metrics import build_model_from_file, CKMetricsCalculator
from metrics_display import MetricsDisplay


def main():
    """Главная функция"""
    if len(sys.argv) < 2:
        print("Использование: python main.py <файл.py> [файл2.py ...]")
        print("Пример: python main.py test_program.py")
        sys.exit(1)
    
    # Построение модели из всех переданных файлов
    from ck_metrics import ModelBuilder
    
    builder = ModelBuilder()
    
    for file_path in sys.argv[1:]:
        if not os.path.exists(file_path):
            print(f"Ошибка: файл '{file_path}' не найден")
            continue
        
        print(f"Обработка файла: {file_path}")
        try:
            builder.build_from_file(file_path)
        except Exception as e:
            print(f"Ошибка при обработке файла '{file_path}': {e}")
            continue
    
    # Получаем финальную модель
    model = builder.model
    
    if not model.classes:
        print("Ошибка: в файлах не найдено ни одного класса")
        sys.exit(1)
    
    # Вычисление метрик
    calculator = CKMetricsCalculator(model)
    display = MetricsDisplay(calculator)
    
    # Отображение результатов
    display.display_summary_table()
    display.display_all_metrics()
    
    # Экспорт в CSV (опционально)
    if len(sys.argv) > 1:
        output_file = "ck_metrics.csv"
        display.export_to_csv(output_file)


if __name__ == "__main__":
    main()

