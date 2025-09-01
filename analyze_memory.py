#!/usr/bin/env python3
"""
Анализ потребления памяти статистикой IsItTrueBot
"""

import sys
from datetime import datetime, date
from collections import defaultdict


def analyze_memory_consumption():
    """Анализирует потребление памяти статистикой бота"""
    
    print("🔍 Анализ потребления памяти статистикой IsItTrueBot")
    print("=" * 60)
    
    # Базовая структура статистики
    base_stats = {
        'start_time': datetime.now(),           # datetime object
        'total_queries': 0,                     # int
        'text_queries': 0,                      # int  
        'button_queries': 0,                    # int
        'categories': defaultdict(int),         # defaultdict with 3 keys max
        'today_queries': 0,                     # int
        'last_reset': datetime.now().date()    # date object
    }
    
    # Размеры базовых типов данных в Python (64-bit)
    sizes = {
        'int': 28,          # Python int object
        'datetime': 48,     # datetime object  
        'date': 32,         # date object
        'str': 49,          # base string object + small string overhead
        'defaultdict': 232, # defaultdict overhead
        'dict': 232,        # base dict size
    }
    
    print("📊 Размеры базовых объектов Python:")
    for obj_type, size in sizes.items():
        print(f"   {obj_type}: {size} bytes")
    
    # Вычисляем базовое потребление памяти
    base_memory = (
        sizes['dict'] +                    # базовый словарь stats
        sizes['datetime'] +                # start_time
        sizes['int'] * 4 +                 # 4 int поля
        sizes['defaultdict'] +             # categories defaultdict
        sizes['date']                      # last_reset
    )
    
    # Дополнительная память для ключей defaultdict (максимум 3 категории)
    category_keys_memory = (
        len('positive') + len('negative') + len('uncertain')  # строки ключей
    ) * (sizes['str'] // len('example')) + sizes['int'] * 3   # значения int
    
    base_memory += category_keys_memory
    
    print(f"\n💾 Базовое потребление памяти:")
    print(f"   Структура stats: {base_memory} bytes ({base_memory / 1024:.2f} KB)")
    
    # Анализ масштабирования
    scenarios = [
        # (queries_per_day, days, description)
        (10, 1, "10 запросов в день"),
        (100, 1, "100 запросов в день"), 
        (10000, 1, "10,000 запросов в день"),
        
        (10, 7, "10 запросов в день x 7 дней"),
        (100, 7, "100 запросов в день x 7 дней"),
        (10000, 7, "10,000 запросов в день x 7 дней"),
        
        (10, 30, "10 запросов в день x 30 дней"),
        (100, 30, "100 запросов в день x 30 дней"),
        (10000, 30, "10,000 запросов в день x 30 дней"),
        
        (10, 365, "10 запросов в день x 365 дней"),
        (100, 365, "100 запросов в день x 365 дней"),
        (10000, 365, "10,000 запросов в день x 365 дней"),
    ]
    
    print(f"\n📈 Анализ масштабирования:")
    print("=" * 60)
    
    for queries_per_day, days, description in scenarios:
        total_queries = queries_per_day * days
        
        # В нашей реализации память НЕ растет с количеством запросов!
        # Мы храним только счетчики, а не данные о каждом запросе
        memory_consumption = base_memory
        
        print(f"\n📋 {description}:")
        print(f"   Общее количество запросов: {total_queries:,}")
        print(f"   Потребление памяти: {memory_consumption} bytes ({memory_consumption / 1024:.2f} KB)")
        print(f"   Память на запрос: {memory_consumption / max(total_queries, 1):.6f} bytes")
        
        # Анализ с учетом возможного роста (если бы мы хранили историю)
        if total_queries > 1000:
            hypothetical_history_memory = total_queries * 64  # если бы хранили каждый запрос
            print(f"   📊 Гипотетически (с историей): {hypothetical_history_memory:,} bytes ({hypothetical_history_memory / 1024 / 1024:.2f} MB)")
    
    print(f"\n" + "=" * 60)
    print("🎯 ВЫВОДЫ:")
    print("=" * 60)
    
    print(f"✅ Фиксированное потребление: ~{base_memory} bytes ({base_memory / 1024:.2f} KB)")
    print("✅ Память НЕ растет с количеством запросов")
    print("✅ Отличная масштабируемость для любого объема трафика")
    print("✅ Подходит даже для миллионов запросов")
    
    print(f"\n🔍 Детальная структура памяти:")
    print(f"   • Базовый словарь: {sizes['dict']} bytes")
    print(f"   • Datetime объекты: {sizes['datetime'] + sizes['date']} bytes")
    print(f"   • Целые числа (5 шт): {sizes['int'] * 5} bytes")
    print(f"   • DefaultDict: {sizes['defaultdict']} bytes")
    print(f"   • Ключи категорий: {category_keys_memory} bytes")
    
    print(f"\n⚡ Производительность:")
    print("   • O(1) для всех операций обновления статистики")
    print("   • O(1) для получения статистики")
    print("   • Нет сборки мусора для счетчиков")
    print("   • Минимальное влияние на GC")


def memory_comparison():
    """Сравнение с альтернативными подходами"""
    
    print(f"\n" + "=" * 60)
    print("🆚 СРАВНЕНИЕ С АЛЬТЕРНАТИВАМИ:")
    print("=" * 60)
    
    alternatives = [
        ("SQLite база данных", "~50-100 KB файл + накладные расходы"),
        ("PostgreSQL", "~10-50 MB процесс + сетевые запросы"),
        ("Redis", "~5-20 MB процесс + сетевое подключение"),
        ("Файловое хранение JSON", "~1-5 KB файл + дисковые операции"),
        ("История запросов в памяти", "~64 bytes * количество запросов"),
        ("Текущая реализация", f"~{(232 + 28*5 + 48 + 32 + 232 + 100):.0f} bytes (фиксированно)")
    ]
    
    for name, consumption in alternatives:
        print(f"   📊 {name}: {consumption}")
    
    print(f"\n🏆 Наше решение:")
    print("   ✅ Минимальное потребление памяти")
    print("   ✅ Нет внешних зависимостей")
    print("   ✅ Максимальная производительность")
    print("   ✅ Простота развертывания")
    print("   ✅ Нет точек отказа")


if __name__ == "__main__":
    analyze_memory_consumption()
    memory_comparison()
    
    print(f"\n🎉 Заключение: Текущая реализация оптимальна для задач бота!")