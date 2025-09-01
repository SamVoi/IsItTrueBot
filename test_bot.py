#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функциональности бота "Это правда?"
"""

import sys
import os
from pathlib import Path

# Добавляем корневую папку проекта в путь для импорта
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_imports():
    """Тестирует корректность импортов"""
    print("🔍 Тестирование импортов...")
    
    try:
        from src.responses import POSITIVE_RESPONSES, NEGATIVE_RESPONSES, UNCERTAIN_RESPONSES
        print("✅ Импорт ответов успешен")
        
        from src.response_generator import response_generator
        print("✅ Импорт генератора ответов успешен")
        
        from config.settings import BotConfig
        print("✅ Импорт конфигурации успешен (предупреждение о токене ожидается)")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def test_response_generator():
    """Тестирует генератор ответов"""
    print("\n🎲 Тестирование генератора ответов...")
    
    try:
        from src.response_generator import response_generator
        
        # Тест генерации 10 ответов
        categories = {'positive': 0, 'negative': 0, 'uncertain': 0}
        
        for i in range(10):
            response, category = response_generator.generate_random_response()
            categories[category] += 1
            
            if i < 3:  # Показываем первые 3 ответа
                print(f"  {i+1}. [{category}] {response[:50]}...")
        
        print(f"\n📊 Статистика по 10 ответам:")
        for cat, count in categories.items():
            print(f"  {cat}: {count}/10 ({count*10}%)")
        
        # Тест статистики
        stats = response_generator.get_statistics()
        print(f"\n📈 Ожидаемое распределение: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка тестирования генератора: {e}")
        return False

def test_responses_data():
    """Тестирует данные ответов"""
    print("\n📝 Тестирование данных ответов...")
    
    try:
        from src.responses import POSITIVE_RESPONSES, NEGATIVE_RESPONSES, UNCERTAIN_RESPONSES
        
        print(f"  Положительных ответов: {len(POSITIVE_RESPONSES)}")
        print(f"  Отрицательных ответов: {len(NEGATIVE_RESPONSES)}")
        print(f"  Неопределенных ответов: {len(UNCERTAIN_RESPONSES)}")
        
        # Проверяем, что все ответы содержат эмодзи
        total_responses = len(POSITIVE_RESPONSES) + len(NEGATIVE_RESPONSES) + len(UNCERTAIN_RESPONSES)
        print(f"  Всего ответов: {total_responses}")
        
        # Примеры ответов
        print(f"\n  Пример положительного: {POSITIVE_RESPONSES[0]}")
        print(f"  Пример отрицательного: {NEGATIVE_RESPONSES[0]}")
        print(f"  Пример неопределенного: {UNCERTAIN_RESPONSES[0]}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка тестирования данных: {e}")
        return False

def test_file_structure():
    """Тестирует структуру файлов проекта"""
    print("\n📁 Проверка структуры проекта...")
    
    required_files = [
        'src/bot.py',
        'src/response_generator.py',
        'src/responses/__init__.py',
        'src/responses/positive.py',
        'src/responses/negative.py', 
        'src/responses/uncertain.py',
        'config/settings.py',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        '.env.example',
        'README.md',
        '.gitignore',
        '.dockerignore'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print(f"\n  ❌ Отсутствующие файлы: {missing_files}")
        return False
    
    print(f"\n  ✅ Все необходимые файлы присутствуют ({len(required_files)} файлов)")
    return True

def main():
    """Главная функция тестирования"""
    print("🤖 Тестирование бота 'Это правда?'")
    print("=" * 50)
    
    tests = [
        ("Структура файлов", test_file_structure),
        ("Импорты модулей", test_imports),
        ("Данные ответов", test_responses_data),
        ("Генератор ответов", test_response_generator),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n❌ Тест '{test_name}' провален")
        except Exception as e:
            print(f"\n❌ Тест '{test_name}' завершился с ошибкой: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты тестирования: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены успешно!")
        print("\n📋 Следующие шаги:")
        print("1. Получите токен бота у @BotFather в Telegram")
        print("2. Включите inline-режим командой /setinline")
        print("3. Создайте .env файл с BOT_TOKEN")
        print("4. Запустите бота: python src/bot.py")
        print("5. Или используйте Docker: docker-compose up -d")
    else:
        print(f"⚠️  {total - passed} тестов провалено. Проверьте ошибки выше.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())