#!/usr/bin/env python3
"""
Точное измерение потребления памяти статистики бота
"""

import sys
from datetime import datetime, date
from collections import defaultdict


def get_size(obj, seen=None):
    """Рекурсивно вычисляет размер объекта в памяти"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    # Важно запомнить, что мы уже видели этот объект
    seen.add(obj_id)

    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])

    return size


def measure_actual_memory():
    """Измеряет фактическое потребление памяти статистики"""
    
    print("🔬 Точное измерение памяти статистики IsItTrueBot")
    print("=" * 60)
    
    # Создаем точно такую же структуру, как в боте
    stats = {
        'start_time': datetime.now(),
        'total_queries': 0,
        'text_queries': 0,
        'button_queries': 0,
        'categories': defaultdict(int),
        'today_queries': 0,
        'last_reset': datetime.now().date()
    }
    
    # Добавляем категории как в реальном использовании
    stats['categories']['positive'] = 0
    stats['categories']['negative'] = 0
    stats['categories']['uncertain'] = 0
    
    print("📊 Размеры отдельных компонентов:")
    print(f"   datetime.now(): {sys.getsizeof(stats['start_time'])} bytes")
    print(f"   int (0): {sys.getsizeof(0)} bytes")
    print(f"   date.today(): {sys.getsizeof(stats['last_reset'])} bytes")
    print(f"   defaultdict: {sys.getsizeof(stats['categories'])} bytes")
    print(f"   базовый dict: {sys.getsizeof({})} bytes")
    
    # Измеряем полный размер
    total_size = get_size(stats)
    
    print(f"\n💾 Общее потребление памяти:")
    print(f"   Полная структура: {total_size} bytes ({total_size / 1024:.3f} KB)")
    
    # Симулируем работу с различным объемом запросов
    scenarios = [
        (10, "Малая нагрузка"),
        (100, "Средняя нагрузка"), 
        (10000, "Высокая нагрузка"),
        (1000000, "Экстремальная нагрузка")
    ]
    
    print(f"\n📈 Симуляция различных нагрузок:")
    print("-" * 60)
    
    for queries, description in scenarios:
        # Копируем базовую структуру
        test_stats = {
            'start_time': datetime.now(),
            'total_queries': queries,
            'text_queries': queries // 2,
            'button_queries': queries // 2,
            'categories': defaultdict(int),
            'today_queries': min(queries, 10000),  # дневной лимит
            'last_reset': datetime.now().date()
        }
        
        # Распределяем по категориям (40%/40%/20%)
        test_stats['categories']['positive'] = int(queries * 0.4)
        test_stats['categories']['negative'] = int(queries * 0.4) 
        test_stats['categories']['uncertain'] = int(queries * 0.2)
        
        size = get_size(test_stats)
        
        print(f"📊 {description} ({queries:,} запросов):")
        print(f"   Память: {size} bytes ({size / 1024:.3f} KB)")
        print(f"   На запрос: {size / queries:.6f} bytes")
        print()
    
    # Измеряем накладные расходы на большие числа
    print("🔢 Влияние размера чисел на память:")
    print("-" * 40)
    
    number_tests = [0, 100, 10000, 1000000, 100000000]
    for num in number_tests:
        size = sys.getsizeof(num)
        print(f"   {num:>12,}: {size} bytes")
    
    print(f"\n✅ Вывод: Память практически не зависит от количества запросов!")
    print(f"📈 Максимальное отклонение: ~{max([sys.getsizeof(n) for n in number_tests]) - min([sys.getsizeof(n) for n in number_tests])} bytes")


def memory_efficiency_analysis():
    """Анализ эффективности использования памяти"""
    
    print(f"\n" + "=" * 60)
    print("⚡ АНАЛИЗ ЭФФЕКТИВНОСТИ:")
    print("=" * 60)
    
    base_stats = {
        'start_time': datetime.now(),
        'total_queries': 0,
        'text_queries': 0,
        'button_queries': 0,
        'categories': defaultdict(int),
        'today_queries': 0,
        'last_reset': datetime.now().date()
    }
    
    base_size = get_size(base_stats)
    
    # Сравнение с полноценной базой данных
    sqlite_overhead = 50 * 1024  # ~50KB для SQLite
    postgres_overhead = 20 * 1024 * 1024  # ~20MB для PostgreSQL
    redis_overhead = 10 * 1024 * 1024  # ~10MB для Redis
    
    print(f"📊 Сравнение эффективности памяти:")
    print(f"   Наша реализация: {base_size:,} bytes")
    print(f"   SQLite (минимум): {sqlite_overhead:,} bytes ({sqlite_overhead / base_size:.0f}x больше)")
    print(f"   PostgreSQL (минимум): {postgres_overhead:,} bytes ({postgres_overhead / base_size:.0f}x больше)")
    print(f"   Redis (минимум): {redis_overhead:,} bytes ({redis_overhead / base_size:.0f}x больше)")
    
    print(f"\n🎯 Преимущества текущего подхода:")
    print("   ✅ Нулевая задержка (все в памяти)")
    print("   ✅ Нет сетевых запросов")  
    print("   ✅ Нет дисковых операций")
    print("   ✅ Нет зависимостей от внешних сервисов")
    print("   ✅ Простота развертывания")
    print("   ✅ Высочайшая надежность")
    
    print(f"\n⚠️ Ограничения:")
    print("   • Данные теряются при перезапуске")
    print("   • Нет истории запросов")
    print("   • Нет персистентности")
    
    print(f"\n🏆 Идеальное решение для:")
    print("   ✅ Мониторинга в реальном времени")
    print("   ✅ Быстрой диагностики")
    print("   ✅ Минимального потребления ресурсов")
    print("   ✅ Максимальной производительности")


if __name__ == "__main__":
    measure_actual_memory()
    memory_efficiency_analysis()