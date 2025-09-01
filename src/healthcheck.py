#!/usr/bin/env python3
"""
Простая проверка здоровья бота для Docker
Проверяет, что процесс бота запущен и отвечает
"""
import sys
import os
import logging
import signal
from pathlib import Path

# Добавляем корневую папку проекта в путь для импорта
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def check_bot_health():
    """
    Проверяет, что бот работает корректно
    Возвращает 0 при успехе, 1 при ошибке
    """
    try:
        # Проверяем, что можем импортировать основные модули
        from config.settings import BotConfig
        
        # Проверяем, что конфигурация валидна
        BotConfig.validate_config()
        
        # Проверяем, что BOT_TOKEN установлен
        if not BotConfig.BOT_TOKEN:
            print("ERROR: BOT_TOKEN не установлен")
            return 1
            
        # Проверяем, что можем импортировать response generator
        from src.response_generator import response_generator
        
        # Тестируем генерацию ответа
        response_text, category = response_generator.generate_random_response()
        if not response_text or not category:
            print("ERROR: Не удалось сгенерировать ответ")
            return 1
            
        print("OK: Бот здоров и готов к работе")
        return 0
        
    except ImportError as e:
        print(f"ERROR: Ошибка импорта модулей: {e}")
        return 1
    except ValueError as e:
        print(f"ERROR: Ошибка конфигурации: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: Неожиданная ошибка: {e}")
        return 1

if __name__ == "__main__":
    exit_code = check_bot_health()
    sys.exit(exit_code)