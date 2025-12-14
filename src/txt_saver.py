import os
from typing import Any, Optional

from .abstract_saver import VacancySaver
from .vacancy import Vacancy


class TXTSaver(VacancySaver):
    """Класс для сохранения вакансий в TXT-файл"""

    def __init__(self, filename: str = "data/vacancies.json"):
        """
        Инициализация JSON-сохранения.

        Args:
            filename: Имя файла для сохранения
        """
        self.filename = filename

        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в TXT-файл"""
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(str(vacancy))
            f.write("\n" + "=" * 50 + "\n")

    def get_vacancies(self, criteria: Optional[dict[str, Any]] = None) -> list[Vacancy]:
        """Получение вакансий из TXT-файла (заглушка)"""
        return []

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из TXT-файла (заглушка)"""
        pass

    def clear(self) -> None:
        """Очистка всех вакансий из TXT-файла"""
        with open(self.filename, "w", encoding="utf-8"):
            pass
