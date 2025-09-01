import sys
import logging
from pathlib import Path

# Добавляем корневую папку проекта в путь для импорта
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultsButton
from telegram.ext import Application, InlineQueryHandler, ContextTypes
from config.settings import BotConfig
from src.response_generator import response_generator


class IsItTrueBot:
    """
    Основной класс бота "Это правда?"
    Обрабатывает inline-запросы и возвращает случайные "фактчекинговые" ответы.
    """
    
    def __init__(self):
        # Настройка логирования
        BotConfig.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Проверяем конфигурацию перед созданием бота
        try:
            BotConfig.validate_config()
        except ValueError as e:
            self.logger.error(f"Ошибка конфигурации: {e}")
            raise
        
        # Создание приложения бота
        # После валидации config мы знаем, что BOT_TOKEN не None
        bot_token = BotConfig.BOT_TOKEN
        assert bot_token is not None, "BOT_TOKEN должен быть установлен после валидации"
        self.application = Application.builder().token(bot_token).build()
        
        # Регистрация обработчиков
        self._register_handlers()
        
        self.logger.info("Бот 'Это правда?' инициализирован")
    
    def _register_handlers(self):
        """Регистрирует обработчики событий бота"""
        # Обработчик inline-запросов
        inline_handler = InlineQueryHandler(self.handle_inline_query)
        self.application.add_handler(inline_handler)
    
    async def handle_inline_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обрабатывает inline-запросы пользователей.
        
        Args:
            update: Объект обновления от Telegram
            context: Контекст бота
        """
        # Проверяем, что inline_query существует
        if not update.inline_query:
            self.logger.warning("Получен update без inline_query")
            return
            
        query = update.inline_query.query
        user_id = update.inline_query.from_user.id if update.inline_query.from_user else "unknown"
        self.logger.info(f"Получен inline-запрос: '{query}' от пользователя {user_id}")
        
        # НЕ генерируем ответ заранее! Генерируем только при отправке сообщения
        # Создаем результат inline-запроса с нейтральным описанием
        results = [
            InlineQueryResultArticle(
                id="fact_check_result",
                title=BotConfig.INLINE_COMMAND_TEXT,
                description=BotConfig.INLINE_COMMAND_DESCRIPTION,
                input_message_content=InputTextMessageContent(
                    message_text=self._generate_delayed_response(),
                    parse_mode=None
                ),
                thumbnail_url=self._get_neutral_icon_url()
            )
        ]
        
        # Отправляем результат пользователю
        await update.inline_query.answer(
            results,
            cache_time=0,  # Не кешируем результаты для получения разных ответов
            is_personal=True,
            button=InlineQueryResultsButton(
                text="Как это работает?",
                start_parameter="help"
            )
        )
    
    def _generate_delayed_response(self) -> str:
        """
        Генерирует случайный ответ на момент отправки сообщения.
        Этот метод вызывается только когда пользователь нажимает на inline результат.
        
        Returns:
            str: Случайный ответ
        """
        response_text, category = response_generator.generate_random_response()
        self.logger.info(f"Сгенерирован ответ категории '{category}' при отправке: {response_text[:50]}...")
        return response_text
    
    def _get_neutral_icon_url(self) -> str:
        """
        Возвращает нейтральную иконку, которая не выдает результат заранее.
        
        Returns:
            str: URL нейтральной иконки
        """
        # Используем нейтральную иконку вопроса для всех результатов
        return 'https://img.icons8.com/color/48/question-mark.png'
    
    def _get_category_icon_url(self, category: str) -> str:
        """
        Возвращает URL иконки для категории ответа.
        
        Args:
            category: Категория ответа
            
        Returns:
            str: URL иконки
        """
        # Можно использовать разные иконки для разных категорий
        icons = {
            'positive': 'https://img.icons8.com/color/48/checkmark.png',
            'negative': 'https://img.icons8.com/color/48/cancel.png', 
            'uncertain': 'https://img.icons8.com/color/48/question-mark.png'
        }
        return icons.get(category, icons['uncertain'])
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик ошибок бота.
        
        Args:
            update: Объект обновления
            context: Контекст с информацией об ошибке
        """
        self.logger.error(f"Ошибка при обработке обновления: {context.error}")
        
        # Если ошибка связана с inline-запросом, отправляем пустой результат
        if isinstance(update, Update) and update.inline_query:
            try:
                await update.inline_query.answer([])
            except Exception as e:
                self.logger.error(f"Не удалось отправить пустой ответ на inline-запрос: {e}")
    
    def run(self):
        """Запускает бота"""
        self.logger.info("Запуск бота 'Это правда?'...")
        
        # Добавляем обработчик ошибок
        self.application.add_error_handler(self.error_handler)
        
        # Запускаем бота
        self.application.run_polling(
            allowed_updates=['inline_query']
        )


def main():
    """Главная функция для запуска бота"""
    try:
        bot = IsItTrueBot()
        bot.run()
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем")
    except Exception as e:
        logging.error(f"Критическая ошибка при запуске бота: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()