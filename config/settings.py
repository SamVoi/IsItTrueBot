import os
import sys
import logging
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


class BotConfig:
    """
    Конфигурация бота "Это правда?"
    """
    
    # Токен бота (обязательный параметр)
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # Настройки логирования
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Настройки бота
    BOT_USERNAME = os.getenv('BOT_USERNAME', 'Is_ItTrue_Bot')
    
    # Команды бота
    INLINE_COMMAND_TEXT = "Это правда?"
    INLINE_COMMAND_DESCRIPTION = "Проверить достоверность информации"
    
    # Настройки inline-ответов
    MAX_INLINE_RESULTS = 1  # Показываем только одну команду
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Проверяет корректность конфигурации.
        
        Returns:
            bool: True если конфигурация корректна
        """
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не установлен! Укажите токен бота в переменной окружения.")
        
        return True
    
    @classmethod
    def setup_logging(cls):
        """
        Настраивает логирование для бота.
        """
        logging.basicConfig(
            format=cls.LOG_FORMAT,
            level=getattr(logging, cls.LOG_LEVEL, logging.INFO)
        )
        
        # Устанавливаем уровень логирования для telegram бота
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("telegram").setLevel(logging.INFO)


# Проверяем конфигурацию при импорте (только если не в режиме тестирования)
if __name__ != "__main__" and "test" not in sys.modules:
    try:
        BotConfig.validate_config()
    except ValueError as e:
        print(f"Ошибка конфигурации: {e}")
        print("Создайте файл .env с BOT_TOKEN=ваш_токен_бота")
        # Не выходим при импорте для тестирования