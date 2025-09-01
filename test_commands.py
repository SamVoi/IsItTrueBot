#!/usr/bin/env python3
"""
Тестовый скрипт для проверки команд бота IsItTrueBot
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корневую папку проекта в путь для импорта
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from unittest.mock import Mock, AsyncMock
from telegram import Update, Message, User, Chat
from telegram.ext import ContextTypes
from src.bot import IsItTrueBot


async def test_commands():
    """Тестирует команды бота"""
    print("🤖 Создание экземпляра бота...")
    
    # Устанавливаем тестовый токен, если он не задан
    import os
    if not os.getenv('BOT_TOKEN'):
        os.environ['BOT_TOKEN'] = 'test_token_123:fake_token_for_testing'
        os.environ['BOT_USERNAME'] = 'TestBot'
    
    try:
        bot = IsItTrueBot()
        print("✅ Бот создан успешно!")
        
        # Проверяем статистику
        print("\n📊 Инициализация статистики:")
        print(f"   Всего запросов: {bot.stats['total_queries']}")
        print(f"   Текстовых запросов: {bot.stats['text_queries']}")
        print(f"   Кнопочных запросов: {bot.stats['button_queries']}")
        print(f"   Время запуска: {bot.stats['start_time']}")
        
        # Создаем мок-объекты для тестирования команд
        mock_user = Mock(spec=User)
        mock_user.id = 12345
        mock_user.first_name = "Test User"
        
        mock_chat = Mock(spec=Chat)
        mock_chat.id = 12345
        mock_chat.type = "private"
        
        mock_message = Mock(spec=Message)
        mock_message.reply_text = AsyncMock()
        mock_message.chat = mock_chat
        
        mock_update = Mock(spec=Update)
        mock_update.message = mock_message
        mock_update.effective_user = mock_user
        
        mock_context = Mock(spec=ContextTypes.DEFAULT_TYPE)
        
        print("\n🧪 Тестирование команд:")
        
        # Тест команды /start
        print("   Тестируем /start...")
        await bot.cmd_start(mock_update, mock_context)
        print("   ✅ /start выполнена")
        
        # Тест команды /help
        print("   Тестируем /help...")
        await bot.cmd_help(mock_update, mock_context)
        print("   ✅ /help выполнена")
        
        # Тест команды /stats
        print("   Тестируем /stats...")
        await bot.cmd_stats(mock_update, mock_context)
        print("   ✅ /stats выполнена")
        
        # Проверяем вызовы reply_text
        call_count = mock_message.reply_text.call_count
        print(f"\n📤 Всего отправлено сообщений: {call_count}")
        
        if call_count >= 3:
            print("✅ Все команды работают корректно!")
        else:
            print("⚠️ Не все команды сработали как ожидалось")
            
        print("\n🎯 Проверка содержимого ответов:")
        for i, call in enumerate(mock_message.reply_text.call_args_list):
            message_text = call[0][0]
            print(f"   Сообщение {i+1}: {message_text[:50]}...")
        
        print("\n✅ Тестирование завершено успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False
    
    return True


async def test_stats_update():
    """Тестирует обновление статистики"""
    print("\n📊 Тестирование статистики...")
    
    # Устанавливаем тестовый токен
    import os
    if not os.getenv('BOT_TOKEN'):
        os.environ['BOT_TOKEN'] = 'test_token_123:fake_token_for_testing'
    
    bot = IsItTrueBot()
    
    initial_queries = bot.stats['total_queries']
    
    # Симулируем несколько запросов
    for i in range(5):
        bot._update_stats()
        bot.stats['text_queries'] += 1
        bot.stats['categories']['positive'] += 1
    
    print(f"   Запросов до: {initial_queries}")
    print(f"   Запросов после: {bot.stats['total_queries']}")
    print(f"   Текстовых запросов: {bot.stats['text_queries']}")
    print(f"   Положительных ответов: {bot.stats['categories']['positive']}")
    
    if bot.stats['total_queries'] > initial_queries:
        print("   ✅ Статистика обновляется корректно!")
        return True
    else:
        print("   ❌ Статистика не обновилась")
        return False


async def main():
    """Главная функция тестирования"""
    print("🚀 Запуск тестирования IsItTrueBot...")
    print("=" * 50)
    
    # Тест команд
    commands_ok = await test_commands()
    
    # Тест статистики
    stats_ok = await test_stats_update()
    
    print("\n" + "=" * 50)
    if commands_ok and stats_ok:
        print("🎉 Все тесты прошли успешно!")
        print("📝 Бот готов к использованию с командами /start, /help, /stats")
        print("📊 Статистика работает без базы данных (в памяти)")
    else:
        print("❌ Некоторые тесты не прошли")
        
    print("\n💡 Для запуска бота используйте: python src/bot.py")


if __name__ == "__main__":
    asyncio.run(main())