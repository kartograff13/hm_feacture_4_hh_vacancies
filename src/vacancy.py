import re
from typing import Any


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = (
        "_name",
        "_url",
        "_salary",
        "_description",
        "_company",
        "_experience",
        "_employment",
        "_salary_from",
        "_salary_to",
    )

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
        self._name = name
        self._url = url
        self._salary = self._validate_salary(salary)
        self._description = description
        self._company = company
        self._experience = experience
        self._employment = employment
        self._salary_from, self._salary_to = self._parse_salary(salary)

    @property
    def name(self) -> str:
        """Название вакансии"""
        return self._name

    @property
    def url(self) -> str:
        """Ссылка на вакансию"""
        return self._url

    @property
    def salary(self) -> str:
        """Зарплата"""
        return self._salary

    @property
    def description(self) -> str:
        """Описание вакансии"""
        return self._description

    @property
    def company(self) -> str:
        """Компания"""
        return self._company

    @property
    def experience(self) -> str:
        """Требуемый опыт"""
        return self._experience

    @property
    def employment(self) -> str:
        """Тип занятости"""
        return self._employment

    @property
    def salary_from(self) -> int:
        """Минимальная зарплата"""
        return self._salary_from

    @property
    def salary_to(self) -> int:
        """Максимальная зарплата"""
        return self._salary_to

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
        if self._salary_from and self._salary_to:
            return (self._salary_from + self._salary_to) / 2
        elif self._salary_from:
            return float(self._salary_from)
        elif self._salary_to:
            return float(self._salary_to)
        else:
            return 0.0

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        return (
            f"{self._name}\n"
            f"Компания: {self._company}\n"
            f"Зарплата: {self._salary}\n"
            f"Опыт: {self._experience}\n"
            f"Тип занятости: {self._employment}\n"
            f"Ссылка: {self._url}\n"
            f"Описание: {self._description[:200]}...\n"
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразование вакансии в словарь"""
        return {
            "name": self._name,
            "url": self._url,
            "salary": self._salary,
            "description": self._description,
            "company": self._company,
            "experience": self._experience,
            "employment": self._employment,
            "salary_from": self._salary_from,
            "salary_to": self._salary_to,
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
