import re
from typing import Any


class Vacancy:
    """Класс для представления вакансии"""

    def __init__(
        self,
        name: str,
        url: str,
        salary: str,
        description: str,
        company: str = "",
        experience: str = "",
        employment: str = "",
    ):
        """
        Инициализация вакансии.

        Args:
            name: Название вакансии
            url: Ссылка на вакансию
            salary: Зарплата
            description: Описание вакансии
            company: Компания
            experience: Требуемый опыт
            employment: Тип занятости
        """
        self.name = name
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description
        self.company = company
        self.experience = experience
        self.employment = employment
        self.salary_from, self.salary_to = self._parse_salary(salary)

    @staticmethod
    def _validate_salary(salary: str) -> str:
        """Валидация зарплаты.

        Args:
            salary: Строка с информацией о зарплате

        Returns:
            Отформатированная строка с зарплатой
        """
        if not salary or salary.lower() in ["", "не указана", "з/п не указана"]:
            return "Зарплата не указана"
        return salary

    @staticmethod
    def _parse_salary(salary: str) -> tuple[int, int]:
        """
        Парсинг зарплаты для сравнения.

        Args:
            salary: Строка с информацией о зарплате

        Returns:
            Кортеж (минимальная зарплата, максимальная зарплата)
        """
        if salary == "Зарплата не указана":
            return 0, 0

        numbers = re.findall(r"\d+", salary.replace(" ", ""))
        numbers = list(map(int, numbers))

        if len(numbers) == 0:
            return 0, 0
        elif len(numbers) == 1:
            return numbers[0], numbers[0]
        else:
            return min(numbers), max(numbers)

    @property
    def avg_salary(self) -> float:
        """Средняя зарплата для сравнения"""
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) / 2
        elif self.salary_from:
            return float(self.salary_from)
        elif self.salary_to:
            return float(self.salary_to)
        else:
            return 0.0

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        return (
            f"{self.name}\n"
            f"Компания: {self.company}\n"
            f"Зарплата: {self.salary}\n"
            f"Опыт: {self.experience}\n"
            f"Тип занятости: {self.employment}\n"
            f"Ссылка: {self.url}\n"
            f"Описание: {self.description[:200]}...\n"
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразование вакансии в словарь"""
        return {
            "name": self.name,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
            "company": self.company,
            "experience": self.experience,
            "employment": self.employment,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Vacancy":
        """Создание вакансии из словаря"""
        return cls(
            name=data.get("name", ""),
            url=data.get("url", ""),
            salary=data.get("salary", ""),
            description=data.get("description", ""),
            company=data.get("company", ""),
            experience=data.get("experience", ""),
            employment=data.get("employment", ""),
        )

    @classmethod
    def cast_to_object_list(cls, vacancies_data: list[dict[str, Any]]) -> list["Vacancy"]:
        """Преобразование списка словарей в список объектов Vacancy."""
        return [cls.from_dict(vacancy) for vacancy in vacancies_data]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary < other.avg_salary

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary > other.avg_salary

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary >= other.avg_salary
