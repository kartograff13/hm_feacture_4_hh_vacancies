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
        self._filename = filename
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

    @property
    def filename(self) -> str:
        """Получение имени файла"""
        return self._filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в CSV-файл"""
        file_exists = os.path.isfile(self._filename)

        with open(self._filename, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            if not file_exists:
                writer.writerow(["name", "url", "salary", "description", "company", "experience", "employment"])

            writer.writerow(
                [
                    vacancy.name,
                    vacancy.url,
                    vacancy.salary,
                    vacancy.description[:500],
                    vacancy.company,
                    vacancy.experience,
                    vacancy.employment,
                ]
            )

    def get_vacancies(self, criteria: Optional[dict[str, Any]] = None) -> list[Vacancy]:
        """Получение вакансий из CSV-файла"""
        vacancies: list[Vacancy] = []

        if not os.path.exists(self._filename):
            return vacancies

        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=";", quotechar='"')
                next(reader, None)

                for row in reader:
                    if len(row) >= 7:
                        vacancy = Vacancy(
                            name=row[0],
                            url=row[1],
                            salary=row[2],
                            description=row[3],
                            company=row[4],
                            experience=row[5],
                            employment=row[6],
                        )
                        vacancies.append(vacancy)

        except (FileNotFoundError, csv.Error):
            return []

        if criteria:
            vacancies = self._filter_vacancies(vacancies, criteria)

        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из CSV-файла"""
        vacancies = self.get_vacancies()

        updated_vacancies = [v for v in vacancies if v.url != vacancy.url]

        self._save_all_vacancies(updated_vacancies)

    def clear(self) -> None:
        """Очистка всех вакансий из CSV-файла"""
        with open(self._filename, "w", encoding="utf-8", newline="") as f:
            f.write("")

    def _save_all_vacancies(self, vacancies: list[Vacancy]) -> None:
        """Сохранение всех вакансий в CSV-файл"""
        with open(self._filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["name", "url", "salary", "description", "company", "experience", "employment"])

            for vacancy in vacancies:
                writer.writerow(
                    [
                        vacancy.name,
                        vacancy.url,
                        vacancy.salary,
                        vacancy.description[:500],
                        vacancy.company,
                        vacancy.experience,
                        vacancy.employment,
                    ]
                )

    @staticmethod
    def _filter_vacancies(vacancies: list[Vacancy], criteria: dict[str, Any]) -> list[Vacancy]:
        """Фильтрация вакансий по критериям"""
        filtered = vacancies

        if "keyword" in criteria:
            keyword = criteria["keyword"].lower()
            filtered = [v for v in filtered if keyword in v.name.lower() or keyword in v.description.lower()]

        if "min_salary" in criteria:
            min_salary = criteria["min_salary"]
            filtered = [v for v in filtered if v.salary_from and v.salary_from >= min_salary]

        if "company" in criteria:
            company = criteria["company"].lower()
            filtered = [v for v in filtered if company in v.company.lower()]

        return filtered
