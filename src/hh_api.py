from typing import Any, Optional, Union, cast

import requests

from .abstract_api import JobAPI


class HeadHunterAPI(JobAPI):
    """Класс для работы с API HeadHunter"""

    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "VacancyParser/1.0 (maksym_krasovskiy@ya.ru)"})

    def connect(self) -> None:
        """Подключение к API HH"""
        try:
            response = self.session.get(f"{self.BASE_URL}?text=test")
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка подключения к API HH.ru: {e}")

    def get_vacancies(self, search_query: str, area: int = 113, per_page: int = 100) -> list[dict[str, Any]]:
        """
        Получение вакансий по поисковому запросу.

        Args:
            search_query: Поисковый запрос
            area: Код региона (113 - Россия)
            per_page: Количество вакансий на странице

        Returns:
            Список вакансий в формате JSON
        """
        params: dict[str, Union[str, int]] = {"text": search_query, "area": area, "per_page": per_page, "page": 0}

        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            vacancies = data.get("items", [])

            detailed_vacancies = []
            for vacancy in vacancies:
                if vacancy_url := vacancy.get("url"):
                    detailed_vacancy = self._get_vacancy_details(vacancy_url)
                    if detailed_vacancy:
                        detailed_vacancies.append(detailed_vacancy)

            return self.format_vacancies(detailed_vacancies or vacancies)

        except requests.RequestException as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []

    def _get_vacancy_details(self, vacancy_url: str) -> Optional[dict[str, Any]]:
        """Получение детальной информации о вакансии"""
        try:
            response = self.session.get(vacancy_url)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
        except requests.RequestException:
            return None

    def format_vacancies(self, raw_vacancies: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Форматирование вакансий HH в единый формат.

        Args:
            raw_vacancies: Список сырых данных вакансий

        Returns:
            Список отформатированных вакансий
        """
        formatted_vacancies = []

        for vacancy in raw_vacancies:
            salary_data = vacancy.get("salary")
            salary = None
            salary_from = None
            salary_to = None

            if salary_data:
                salary_from = salary_data.get("from")
                salary_to = salary_data.get("to")
                currency = salary_data.get("currency", "RUR")

                if salary_from is not None and salary_to is not None:
                    salary = f"{salary_from} - {salary_to} {currency}"
                elif salary_from is not None:
                    salary = f"от {salary_from} {currency}"
                elif salary_to is not None:
                    salary = f"до {salary_to} {currency}"

            formatted_vacancy = {
                "id": vacancy.get("id"),
                "name": vacancy.get("name"),
                "url": vacancy.get("alternate_url") or vacancy.get("url"),
                "salary": salary or "Зарплата не указана",
                "salary_from": salary_from,
                "salary_to": salary_to,
                "description": self._clean_description(vacancy.get("description")),
                "requirements": self._get_requirements(vacancy),
                "company": vacancy.get("employer", {}).get("name"),
                "experience": vacancy.get("experience", {}).get("name"),
                "employment": vacancy.get("employment", {}).get("name"),
                "schedule": vacancy.get("schedule", {}).get("name"),
                "published_at": vacancy.get("published_at"),
            }
            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies

    @staticmethod
    def _clean_description(description: Optional[str]) -> str:
        """Очистка описания от HTML-тегов

        Args:
            description: Текст описания с HTML-тегами

        Returns:
            Очищенный от HTML-тегов текст
        """
        if not description:
            return ""

        import re

        clean = re.compile("<.*?>")
        return re.sub(clean, "", description)

    @staticmethod
    def _get_requirements(vacancy: dict[str, Any]) -> str:
        """Извлечение требований из вакансии

        Args:
            vacancy: Словарь с данными вакансии

        Returns:
            Строка с требованиями и обязанностями
        """
        snippet = vacancy.get("snippet", {})
        requirement = snippet.get("requirement")
        responsibility = snippet.get("responsibility")

        requirements = []
        if requirement:
            requirements.append(f"Требования: {requirement}")
        if responsibility:
            requirements.append(f"Обязанности: {responsibility}")

        if requirements:
            return " ".join(requirements)
        else:
            description = vacancy.get("description", "")
            return (description[:200] + "...") if description else ""
