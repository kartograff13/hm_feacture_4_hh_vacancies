from abc import ABC, abstractmethod
from typing import Any


class JobAPI(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def connect(self) -> None:
        """Подключение к API"""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str) -> list[dict[str, Any]]:
        """Получение вакансий по поисковому запросу"""
        pass

    @abstractmethod
    def format_vacancies(self, raw_vacancies: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Форматирование вакансий в единый формат"""
        pass
