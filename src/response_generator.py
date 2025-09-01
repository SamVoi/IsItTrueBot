import random
from typing import Dict, List, Tuple
from .responses import POSITIVE_RESPONSES, NEGATIVE_RESPONSES, UNCERTAIN_RESPONSES


class ResponseGenerator:
    """
    Генератор случайных ответов для бота "Это правда?"
    Имитирует авторитетный фактчекинг через честный рандом.
    """
    
    def __init__(self):
        # Весовые коэффициенты для категорий ответов
        self.category_weights = {
            'positive': 0.5,    # 50% - положительные ответы
            'negative': 0.3,    # 30% - отрицательные ответы  
            'uncertain': 0.2    # 20% - неопределенные ответы
        }
        
        # Словарь с ответами по категориям
        self.responses = {
            'positive': POSITIVE_RESPONSES,
            'negative': NEGATIVE_RESPONSES,
            'uncertain': UNCERTAIN_RESPONSES
        }
    
    def generate_random_response(self) -> Tuple[str, str]:
        """
        Генерирует случайный ответ с авторитетным тоном.
        
        Returns:
            Tuple[str, str]: (response_text, category)
        """
        # Выбираем категорию с учетом весов
        categories = list(self.category_weights.keys())
        weights = list(self.category_weights.values())
        
        selected_category = random.choices(categories, weights=weights)[0]
        
        # Выбираем случайный ответ из выбранной категории
        response_text = random.choice(self.responses[selected_category])
        
        return response_text, selected_category
    
    def get_response_by_category(self, category: str) -> str:
        """
        Возвращает случайный ответ из определенной категории.
        
        Args:
            category: Категория ответа ('positive', 'negative', 'uncertain')
            
        Returns:
            str: Текст ответа
        """
        if category not in self.responses:
            raise ValueError(f"Неизвестная категория: {category}")
        
        return random.choice(self.responses[category])
    
    def get_statistics(self) -> Dict[str, float]:
        """
        Возвращает статистику распределения ответов по категориям.
        
        Returns:
            Dict[str, float]: Словарь с весами категорий
        """
        return self.category_weights.copy()


# Создаем глобальный экземпляр генератора для использования в боте
response_generator = ResponseGenerator()