from src.vacancy import Vacancy


class TestVacancy:
    """Тесты для класса Vacancy"""

    def test_vacancy_creation(self) -> None:
        """Тест создания вакансии"""
        vacancy = Vacancy(
            name="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary="150000 - 200000 руб.",
            description="Разработка на Python",
            company="Yandex",
            experience="1-3 года",
            employment="Полная занятость",
        )

        assert vacancy.name == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary == "150000 - 200000 руб."
        assert vacancy.company == "Yandex"
        assert vacancy.experience == "1-3 года"
        assert vacancy.employment == "Полная занятость"

    def test_vacancy_salary_parsing(self) -> None:
        """Тест парсинга зарплаты"""
        vacancy1 = Vacancy("Test", "url", "100000 - 150000 руб.", "desc")
        assert vacancy1.salary_from == 100000
        assert vacancy1.salary_to == 150000

        vacancy2 = Vacancy("Test", "url", "от 120000 руб.", "desc")
        assert vacancy2.salary_from == 120000
        assert vacancy2.salary_to == 120000

        vacancy3 = Vacancy("Test", "url", "до 180000 руб.", "desc")
        assert vacancy3.salary_from == 180000
        assert vacancy3.salary_to == 180000

        vacancy4 = Vacancy("Test", "url", "Зарплата не указана", "desc")
        assert vacancy4.salary_from == 0
        assert vacancy4.salary_to == 0

    def test_vacancy_avg_salary(self) -> None:
        """Тест расчета средней зарплаты"""
        vacancy1 = Vacancy("Test", "url", "100000 - 150000 руб.", "desc")
        assert vacancy1.avg_salary == 125000.0

        vacancy2 = Vacancy("Test", "url", "от 120000 руб.", "desc")
        assert vacancy2.avg_salary == 120000.0

        vacancy3 = Vacancy("Test", "url", "Зарплата не указана", "desc")
        assert vacancy3.avg_salary == 0.0

    def test_vacancy_comparison_operators(self) -> None:
        """Тест операторов сравнения"""
        vacancy1 = Vacancy("Test1", "url1", "100000 - 150000 руб.", "desc1")
        vacancy2 = Vacancy("Test2", "url2", "120000 - 180000 руб.", "desc2")
        vacancy3 = Vacancy("Test3", "url3", "100000 - 150000 руб.", "desc3")

        assert vacancy2 > vacancy1
        assert vacancy1 < vacancy2
        assert vacancy1 == vacancy3
        assert vacancy1 <= vacancy2
        assert vacancy2 >= vacancy1

    def test_vacancy_to_dict(self) -> None:
        """Тест преобразования в словарь"""
        vacancy = Vacancy(
            name="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary="150000 - 200000 руб.",
            description="Разработка на Python",
            company="Yandex",
        )

        data = vacancy.to_dict()

        assert data["name"] == "Python Developer"
        assert data["url"] == "https://hh.ru/vacancy/123"
        assert data["salary"] == "150000 - 200000 руб."
        assert data["company"] == "Yandex"
        assert "salary_from" in data
        assert "salary_to" in data

    def test_vacancy_from_dict(self) -> None:
        """Тест создания из словаря"""
        data = {
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary": "150000 - 200000 руб.",
            "description": "Разработка на Python",
            "company": "Yandex",
            "experience": "1-3 года",
            "employment": "Полная занятость",
        }

        vacancy = Vacancy.from_dict(data)

        assert vacancy.name == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.company == "Yandex"

    def test_vacancy_cast_to_object_list(self) -> None:
        """Тест преобразования списка словарей в список объектов"""
        data_list = [
            {
                "name": "Python Developer",
                "url": "https://hh.ru/vacancy/123",
                "salary": "150000 - 200000 руб.",
                "description": "Desc1",
                "company": "Company1",
            },
            {
                "name": "Java Developer",
                "url": "https://hh.ru/vacancy/456",
                "salary": "120000 - 180000 руб.",
                "description": "Desc2",
                "company": "Company2",
            },
        ]

        vacancies = Vacancy.cast_to_object_list(data_list)

        assert len(vacancies) == 2
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0].name == "Python Developer"
        assert vacancies[1].name == "Java Developer"

    def test_vacancy_str_representation(self) -> None:
        """Тест строкового представления"""
        vacancy = Vacancy(
            name="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary="150000 - 200000 руб.",
            description="Разработка на Python и Django. Требуется опыт работы от 1 года.",
            company="Yandex",
            experience="1-3 года",
            employment="Полная занятость",
        )

        result = str(vacancy)

        assert "Python Developer" in result
        assert "Yandex" in result
        assert "150000 - 200000" in result
        assert "https://hh.ru/vacancy/123" in result
