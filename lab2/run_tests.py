"""
Скрипт для запуска всех тестовых программ и демонстрации корректности модуля
"""

import os
import sys
from ck_metrics import ModelBuilder, CKMetricsCalculator
from metrics_display import MetricsDisplay


def run_test(test_file: str):
    """Запустить тест для одного файла"""
    print("\n" + "="*80)
    print(f"ТЕСТ: {test_file}")
    # print("="*80)
    
    if not os.path.exists(test_file):
        print(f"Ошибка: файл '{test_file}' не найден")
        return False
    
    try:
        builder = ModelBuilder()
        builder.build_from_file(test_file)
        model = builder.model
        
        if not model.classes:
            print("Предупреждение: в файле не найдено классов")
            return False
        
        calculator = CKMetricsCalculator(model)
        display = MetricsDisplay(calculator)
        
        display.display_summary_table()
        
        return True
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Главная функция"""
    test_files = [
        "test_simple.py",
        "test_inheritance.py",
        "test_coupling.py",
        "test_cohesion.py",
        "test_complex.py"
    ]
    
    print("\n" + "="*80)
    print("ЗАПУСК ВСЕХ ТЕСТОВ ДЛЯ МЕТРИК ЧИДАМБЕРА И КЕМЕРЕРА")
    print("="*80)
    
    results = []
    for test_file in test_files:
        success = run_test(test_file)
        results.append((test_file, success))
    
    # Итоговая сводка
    print("\n" + "="*80)
    print("ИТОГОВАЯ СВОДКА")
    print("="*80)
    
    for test_file, success in results:
        status = "[OK] УСПЕШНО" if success else "[FAIL] ОШИБКА"
        print(f"{status:20} - {test_file}")
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nУспешно: {successful}/{total}")
    
    if successful == total:
        print("\nВсе тесты пройдены успешно!")
        return 0
    else:
        print(f"\nПровалено тестов: {total - successful}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

