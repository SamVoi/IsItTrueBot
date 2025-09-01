import sys
import sys
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Добавляем корневую папку проекта в путь для импорта
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultsButton
from telegram.ext import Application, InlineQueryHandler, ContextTypes, CommandHandler
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
        
        # Простая статистика в памяти (без базы данных)
        self.stats = {
            'start_time': datetime.now(),
            'total_queries': 0,
            'text_queries': 0,
            'button_queries': 0,
            'categories': defaultdict(int),
            'today_queries': 0,
            'last_reset': datetime.now().date()
        }
        
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
        # Обработчик команд
        self.application.add_handler(CommandHandler('start', self.cmd_start))
        self.application.add_handler(CommandHandler('help', self.cmd_help))
        self.application.add_handler(CommandHandler('stats', self.cmd_stats))
        
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
        
        # Обновляем статистику
        self._update_stats()
        
        # Проверяем, есть ли текст запроса после имени бота
        query_text = query.strip()
        has_text_query = bool(query_text)
        
        if has_text_query:
            # Режим с текстом: сразу генерируем ответ с упоминанием запроса
            response_text, category = response_generator.generate_random_response()
            
            # Формируем авторитетный ответ с упоминанием запроса
            formatted_response = self._format_query_response(query_text, response_text, category)
            
            # Обновляем статистику
            self.stats['text_queries'] += 1
            self.stats['categories'][category] += 1
            
            results = [
                InlineQueryResultArticle(
                    id="fact_check_query_result",
                    title=f"Проверка: {query_text[:50]}{'...' if len(query_text) > 50 else ''}",
                    description="Нажмите для получения результата фактчека",
                    input_message_content=InputTextMessageContent(
                        message_text=formatted_response,
                        parse_mode=None
                    ),
                    thumbnail_url=self._get_neutral_icon_url()
                )
            ]
            
            self.logger.info(f"Сгенерирован ответ категории '{category}' для запроса: '{query_text[:30]}...'")
        else:
            # Обычный режим: показываем кнопку для случайного ответа
            self.stats['button_queries'] += 1
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
    
    def _format_query_response(self, query_text: str, response_text: str, category: str) -> str:
        """
        Формирует авторитетный ответ с упоминанием запроса.
        
        Args:
            query_text: Текст запроса пользователя
            response_text: Стандартный ответ бота
            category: Категория ответа
            
        Returns:
            str: Форматированный ответ с упоминанием запроса
        """
        # Формируем итоговый ответ без префикса - только запрос и результат
        formatted_response = f"📝 Запрос: \"{query_text}\"\n\n{response_text}"
        
        return formatted_response
    
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
    
    def _update_stats(self):
        """Обновляет простую статистику"""
        today = datetime.now().date()
        
        # Сбрасываем счетчик на новый день
        if today != self.stats['last_reset']:
            self.stats['today_queries'] = 0
            self.stats['last_reset'] = today
        
        self.stats['total_queries'] += 1
        self.stats['today_queries'] += 1
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        if not update.message:
            return
            
        start_message = (
            "🤖 **Привет! Я бот-фактчекер!**\n\n"
            "📝 **Как использовать:**\n"
            "1️⃣ Обычный режим: Напишите `@{bot_username}` в любом чате и нажмите кнопку\n"
            "2️⃣ Текстовый режим: `@{bot_username} ваш вопрос`\n\n"
            "🎯 **Пример:** `@{bot_username} правда что вода мокрая?`\n\n"
            "ℹ️ Команды: /help - помощь, /stats - статистика"
        ).format(bot_username=BotConfig.BOT_USERNAME or 'bot_name')
        
        await update.message.reply_text(start_message, parse_mode='Markdown')
        user_id = update.effective_user.id if update.effective_user else 'unknown'
        self.logger.info(f"Отправлен ответ на /start пользователю {user_id}")
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        if not update.message:
            return
            
        help_message = (
            "📚 **Помощь по боту-фактчекеру**\n\n"
            "🤔 **Что это такое?**\n"
            "Это шуточный бот, который имитирует фактчекинг через честный рандом. Не принимайте ответы серьёзно!\n\n"
            "📝 **Как пользоваться:**\n"
            "1. Откройте любой чат в Telegram\n"
            "2. Начните печатать: `@{bot_username}`\n"
            "3. Выберите из меню или допишите свой вопрос\n"
            "4. Нажмите на результат\n\n"
            "🎲 **Вероятности:**\n"
            "✅ 40% - положительные ответы\n"
            "❌ 40% - отрицательные ответы\n"
            "⚠️ 20% - неопределённые ответы\n\n"
            "📈 Команды: /stats - статистика бота"
        ).format(bot_username=BotConfig.BOT_USERNAME or 'bot_name')
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
        user_id = update.effective_user.id if update.effective_user else 'unknown'
        self.logger.info(f"Отправлен ответ на /help пользователю {user_id}")
    
    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /stats"""
        if not update.message:
            return
            
        uptime = datetime.now() - self.stats['start_time']
        uptime_str = f"{uptime.days} дн. {uptime.seconds // 3600} ч. {(uptime.seconds % 3600) // 60} мин."
        
        # Вычисляем проценты категорий
        total_responses = sum(self.stats['categories'].values())
        if total_responses > 0:
            positive_pct = (self.stats['categories']['positive'] / total_responses) * 100
            negative_pct = (self.stats['categories']['negative'] / total_responses) * 100
            uncertain_pct = (self.stats['categories']['uncertain'] / total_responses) * 100
        else:
            positive_pct = negative_pct = uncertain_pct = 0
        
        stats_message = (
            "📈 **Статистика бота**\n\n"
            f"🔄 **Время работы:** {uptime_str}\n"
            f"📅 **За сегодня:** {self.stats['today_queries']} запросов\n"
            f"📈 **Всего:** {self.stats['total_queries']} запросов\n\n"
            "📊 **По типам:**\n"
            f"📝 Текстовые: {self.stats['text_queries']}\n"
            f"🔘 Кнопка: {self.stats['button_queries']}\n\n"
        )
        
        if total_responses > 0:
            stats_message += (
                "🎯 **Категории ответов:**\n"
                f"✅ Положительные: {self.stats['categories']['positive']} ({positive_pct:.1f}%)\n"
                f"❌ Отрицательные: {self.stats['categories']['negative']} ({negative_pct:.1f}%)\n"
                f"⚠️ Неопределённые: {self.stats['categories']['uncertain']} ({uncertain_pct:.1f}%)\n"
            )
        
        stats_message += "\n📌 *Статистика обновляется в реальном времени*"
        
        await update.message.reply_text(stats_message, parse_mode='Markdown')
        user_id = update.effective_user.id if update.effective_user else 'unknown'
        self.logger.info(f"Отправлена статистика пользователю {user_id}")
    
    def run(self):
        """Запускает бота"""
        self.logger.info("Запуск бота 'Это правда?'...")
        
        # Добавляем обработчик ошибок
        self.application.add_error_handler(self.error_handler)
        
        # Запускаем бота
        self.application.run_polling(
            allowed_updates=['inline_query', 'message']
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