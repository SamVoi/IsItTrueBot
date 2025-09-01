#!/usr/bin/env python3
"""
Тест для проверки нового функционала обработки текстовых запросов
"""
import sys
from pathlib import Path

# Добавляем корневую папку проекта в путь для импорта
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.bot import IsItTrueBot
from src.response_generator import response_generator

def test_format_query_response():
    """Тестирует форматирование ответов с упоминанием запроса"""
    bot = IsItTrueBot()
    
    # Тестовые данные
    test_cases = [
        {
            'query': 'правда что вода мокрая?',
            'response': '✅ Да, это абсолютно правда согласно проверенным источникам',
            'category': 'positive'
        },
        {
            'query': 'земля плоская?',
            'response': '❌ Нет, это опровергнуто фактчекерами',
            'category': 'negative'
        },
        {
            'query': 'завтра будет дождь?',
            'response': '⚠️ Частично правда, но не хватает важного контекста',
            'category': 'uncertain'
        }
    ]
    
    print("🧪 ТЕСТИРОВАНИЕ ФОРМАТИРОВАНИЯ ОТВЕТОВ С ЗАПРОСАМИ")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        query = test_case['query']
        response = test_case['response']
        category = test_case['category']
        
        formatted = bot._format_query_response(query, response, category)
        
        print(f"\n📝 Тест {i}: {category}")
        print(f"   Запрос: {query}")
        print(f"   Результат:")
        print("   " + "─" * 50)
        for line in formatted.split('\n'):
            print(f"   {line}")
        print("   " + "─" * 50)

def test_response_generation():
    """Тестирует генерацию случайных ответов"""
    print("\n\n🎲 ТЕСТИРОВАНИЕ ГЕНЕРАЦИИ СЛУЧАЙНЫХ ОТВЕТОВ")
    print("=" * 60)
    
    for i in range(3):
        response_text, category = response_generator.generate_random_response()
        print(f"\n{i+1}. Категория: {category}")
        print(f"   Ответ: {response_text}")

def main():
    """Главная функция тестирования"""
    try:
        print("🚀 Запуск тестов для IsItTrueBot")
        print()
        
        test_format_query_response()
        test_response_generation()
        
        print("\n\n✅ Все тесты завершены!")
        print("\n💡 Примеры использования:")
        print("   1. Обычный режим: @bot_name → кнопка → случайный ответ")
        print("   2. Текстовый режим: @bot_name правда что вода мокрая? → ответ с упоминанием запроса")
        print("\n📋 Новый формат ответа (без префикса):")
        print("   📝 Запрос: \"ваш вопрос\"")
        print("   ✅/❌/⚠️ [авторитетный ответ]")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()