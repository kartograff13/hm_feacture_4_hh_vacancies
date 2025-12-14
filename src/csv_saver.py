import csv
import os
from typing import Any, Optional

from .abstract_saver import VacancySaver
from .vacancy import Vacancy


class CSVSaver(VacancySaver):
    """Класс для сохранения вакансий в CSV-файл"""

    def __init__(self, filename: str = "data/vacancies.csv"):
        """
        Инициализация CSV-сохранения.

        Args:
            filename: Имя файла для сохранения
        """
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.fieldnames = [
            "name",
            "url",
            "salary",
            "description",
            "company",
            "experience",
            "employment",
            "salary_from",
            "salary_to",
        ]

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в CSV-файл"""
        vacancies = self.get_vacancies()

        for v in vacancies:
            if v.url == vacancy.url:
                return

        vacancies.append(vacancy)
        self._save_vacancies(vacancies)

    def get_vacancies(self, criteria: Optional[dict[str, Any]] = None) -> list[Vacancy]:
        """Получение вакансий из CSV-файла"""
        vacancies = []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    vacancy = Vacancy.from_dict(row)
                    vacancies.append(vacancy)
        except FileNotFoundError:
            return []

        if criteria:
            vacancies = self._filter_vacancies(vacancies, criteria)

        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из CSV-файла"""
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v.url != vacancy.url]
        self._save_vacancies(vacancies)

    def clear(self) -> None:
        """Очистка всех вакансий из CSV-файла"""
        self._save_vacancies([])

    def _save_vacancies(self, vacancies: list[Vacancy]) -> None:
        """Сохранение вакансий в CSV-файл"""
        with open(self.filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            for vacancy in vacancies:
                writer.writerow(vacancy.to_dict())

    @staticmethod
    def _filter_vacancies(vacancies: list[Vacancy], criteria: dict[str, Any]) -> list[Vacancy]:
        """Фильтрация вакансий по критериям

        Args:
            vacancies: Список вакансий для фильтрации
            criteria: Словарь с критериями фильтрации

        Returns:
            Отфильтрованный список вакансий
        """
        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            matches = True

            for key, value in criteria.items():
                vacancy_value = getattr(vacancy, key, None)

                if isinstance(value, str) and isinstance(vacancy_value, str):
                    if value.lower() not in vacancy_value.lower():
                        matches = False
                        break
                elif vacancy_value != value:
                    matches = False
                    break

            if matches:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies
