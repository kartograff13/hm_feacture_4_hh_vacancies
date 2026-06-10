import json
import os
from typing import Any, Optional, cast

from .abstract_saver import VacancySaver
from .vacancy import Vacancy


class JSONSaver(VacancySaver):
    """Класс для сохранения вакансий в JSON-файл"""

    def __init__(self, filename: str = "data/vacancies.json"):
        """
        Инициализация JSON-сохранения.

        Args:
            filename: Имя файла для сохранения
        """
        self._filename = filename

        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

    @property
    def filename(self) -> str:
        """Получение имени файла"""
        return self._filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в JSON-файл"""
        vacancies = self._load_vacancies()
        vacancy_dict = vacancy.to_dict()

        for v in vacancies:
            if v.get("url") == vacancy.url:
                return

        vacancies.append(vacancy_dict)
        self._save_vacancies(vacancies)

    def get_vacancies(self, criteria: Optional[dict[str, Any]] = None) -> list[Vacancy]:
        """
        Получение вакансий из JSON-файла.

        Args:
            criteria: Критерии фильтрации (например, {'min_salary': 50000})

        Returns:
            Список объектов Vacancy
        """
        vacancies_data = self._load_vacancies()
        vacancies = Vacancy.cast_to_object_list(vacancies_data)

        if criteria:
            vacancies = self._filter_vacancies(vacancies, criteria)

        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из JSON-файла"""
        vacancies = self._load_vacancies()

        index_to_remove = -1
        for i, v in enumerate(vacancies):
            if v.get("url") == vacancy.url:
                index_to_remove = i
                break

        if index_to_remove != -1:
            vacancies.pop(index_to_remove)
            self._save_vacancies(vacancies)

    def clear(self) -> None:
        """Очистка всех вакансий из JSON-файла"""
        self._save_vacancies([])

    def _load_vacancies(self) -> list[dict[str, Any]]:
        """Загрузка вакансий из JSON-файла"""
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                return cast(list[dict[str, Any]], json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_vacancies(self, vacancies: list[dict[str, Any]]) -> None:
        """Сохранение вакансий в JSON-файл"""
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _filter_vacancies(vacancies: list[Vacancy], criteria: dict[str, Any]) -> list[Vacancy]:
        """Фильтрация вакансий по критериям

        Args:
            vacancies: Список вакансий для фильтрации
            criteria: Словарь с критериями фильтрации

        Returns:
            Отфильтрованный список вакансий
        """
        filtered = vacancies

        if "keyword" in criteria:
            keyword = criteria["keyword"].lower()
            filtered = [v for v in filtered if keyword in v.name.lower() or keyword in v.description.lower()]

        if "min_salary" in criteria:
            min_salary = criteria["min_salary"]
            filtered = [v for v in filtered if v.salary_from and v.salary_from >= min_salary]

        if "max_salary" in criteria:
            max_salary = criteria["max_salary"]
            filtered = [v for v in filtered if v.salary_to and v.salary_to <= max_salary]

        if "company" in criteria:
            company = criteria["company"].lower()
            filtered = [v for v in filtered if company in v.company.lower()]

        return filtered
