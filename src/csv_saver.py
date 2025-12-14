import csv
import os
from typing import Any, Optional

from .abstract_saver import VacancySaver
from .vacancy import Vacancy


class CSVSaver(VacancySaver):
    """Класс для сохранения вакансий в CSV-файл"""

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
        """Добавление вакансии в CSV-файл"""
        vacancies = self.get_vacancies()

        for v in vacancies:
            if v.url == vacancy.url:
                return

        vacancies.append(vacancy)
        self._save_vacancies(vacancies)

    def get_vacancies(self, criteria: Optional[dict[str, Any]] = None) -> list[Vacancy]:
        """
        Получение вакансий из CSV-файла.

        Args:
            criteria: Критерии фильтрации (пока не реализовано для CSV)

        Returns:
            Список объектов Vacancy
        """
        if not os.path.exists(self.filename):
            return []

        vacancies = []
        with open(self.filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                vacancy = Vacancy(
                    name=row["name"],
                    url=row["url"],
                    salary=row["salary"],
                    description=row["description"],
                    company=row["company"],
                    experience=row.get("experience", ""),
                    employment=row.get("employment", ""),
                )
                vacancies.append(vacancy)

        if criteria:
            if "keyword" in criteria:
                keyword = criteria["keyword"].lower()
                vacancies = [v for v in vacancies if keyword in v.name.lower() or keyword in v.description.lower()]

        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из CSV-файла"""
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v.url != vacancy.url]
        self._save_vacancies(vacancies)

    def clear(self) -> None:
        """Очистка всех вакансий из CSV-файла"""
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("name,url,salary,description,company,experience,employment\n")

    def _save_vacancies(self, vacancies: list[Vacancy]) -> None:
        """Сохранение вакансий в CSV-файл"""
        with open(self.filename, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "url", "salary", "description", "company", "experience", "employment"])
            for vacancy in vacancies:
                writer.writerow(
                    [
                        vacancy.name,
                        vacancy.url,
                        vacancy.salary,
                        vacancy.description,
                        vacancy.company,
                        vacancy.experience,
                        vacancy.employment,
                    ]
                )
