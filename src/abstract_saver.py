from abc import ABC, abstractmethod
from typing import Any, Optional

from .vacancy import Vacancy


class VacancySaver(ABC):
    """Абстрактный класс для сохранения вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[dict[str, Any]] = None) -> list[Vacancy]:
        """Получение вакансий по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очистка всех вакансий"""
        pass

    def filter_by_salary(self, min_salary: int = 0) -> list[Vacancy]:
        """Фильтрация по зарплате (заглушка для будущего использования с БД)"""
        vacancies = self.get_vacancies()
        return [v for v in vacancies if v.salary_from >= min_salary]

    def sort_by_salary(self, descending: bool = True) -> list[Vacancy]:
        """Сортировка по зарплате (заглушка для будущего использования с БД)"""
        vacancies = self.get_vacancies()
        return sorted(vacancies, reverse=descending)
