import pytest

from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from src.vacancy import Vacancy


class TestUtils:
    """Тесты вспомогательных функций"""

    @pytest.fixture
    def sample_vacancies(self) -> list[Vacancy]:
        """Создание тестовых вакансий"""
        return [
            Vacancy(
                name="Python Developer",
                url="url1",
                salary="100000 - 150000 руб.",
                description="Разработка на Python и Django",
                company="Yandex",
            ),
            Vacancy(
                name="Java Developer",
                url="url2",
                salary="80000 - 120000 руб.",
                description="Разработка на Java и Spring",
                company="Sber",
            ),
            Vacancy(
                name="Data Scientist",
                url="url3",
                salary="120000 - 180000 руб.",
                description="Анализ данных на Python",
                company="Tinkoff",
            ),
            Vacancy(
                name="Frontend Developer",
                url="url4",
                salary="90000 - 140000 руб.",
                description="Разработка на React",
                company="VK",
            ),
        ]

    def test_filter_vacancies_no_filter(self, sample_vacancies: list[Vacancy]) -> None:
        """Тест фильтрации без ключевых слов"""
        filtered = filter_vacancies(sample_vacancies, [])

        assert len(filtered) == 4
        assert filtered == sample_vacancies

    def test_filter_vacancies_with_keywords(self, sample_vacancies: list[Vacancy]) -> None:
        """Тест фильтрации с ключевыми словами"""
        python_vacancies = filter_vacancies(sample_vacancies, ["Python"])

        assert len(python_vacancies) == 2
        for vacancy in python_vacancies:
            assert "Python" in vacancy.name or "Python" in vacancy.description

        developer_vacancies = filter_vacancies(sample_vacancies, ["Developer"])

        assert len(developer_vacancies) == 3
        for vacancy in developer_vacancies:
            assert "Developer" in vacancy.name

        java_sber_vacancies = filter_vacancies(sample_vacancies, ["Java", "Sber"])

        assert len(java_sber_vacancies) == 1
        assert java_sber_vacancies[0].name == "Java Developer"

    def test_filter_vacancies_case_insensitive(self, sample_vacancies: list[Vacancy]) -> None:
        """Тест регистронезависимой фильтрации"""
        filtered = filter_vacancies(sample_vacancies, ["python"])

        assert len(filtered) == 2

    def test_get_vacancies_by_salary_no_range(self, sample_vacancies: list[Vacancy]) -> None:
        """Тест фильтрации по зарплате без диапазона"""
        result = get_vacancies_by_salary(sample_vacancies, "")

        assert len(result) == 4
        assert result == sample_vacancies

    def test_get_vacancies_by_salary_with_range(self, sample_vacancies: list[Vacancy]) -> None:
        """Тест фильтрации по диапазону зарплат"""
        result = get_vacancies_by_salary(sample_vacancies, "100000-130000")

        assert len(result) == 0

    def test_get_vacancies_by_salary_invalid_range(self, sample_vacancies: list[Vacancy]) -> None:
        """Тест фильтрации с неверным форматом диапазона"""
        result = get_vacancies_by_salary(sample_vacancies, "invalid-format")

        assert len(result) == 4

    def test_get_vacancies_by_salary_edge_cases(self) -> None:
        """Тест граничных случаев фильтрации по зарплате"""
        vacancies = [
            Vacancy("V1", "url1", "от 50000 руб.", "Desc1", "C1"),
            Vacancy("V2", "url2", "до 100000 руб.", "Desc2", "C2"),
            Vacancy("V3", "url3", "80000 - 120000 руб.", "Desc3", "C3"),
            Vacancy("V4", "url4", "Зарплата не указана", "Desc4", "C4"),
        ]

        result = get_vacancies_by_salary(vacancies, "60000-90000")

        assert len(result) == 0

    def test_sort_vacancies(self, sample_vacancies: list[Vacancy]) -> None:
        """Тест сортировки вакансий"""
        sorted_list = sort_vacancies(sample_vacancies)

        for i in range(len(sorted_list) - 1):
            assert sorted_list[i].avg_salary >= sorted_list[i + 1].avg_salary

        assert sorted_list[0].name == "Data Scientist"
        assert sorted_list[1].name == "Python Developer"
        assert sorted_list[2].name == "Frontend Developer"
        assert sorted_list[3].name == "Java Developer"

    def test_get_top_vacancies(self, sample_vacancies: list[Vacancy]) -> None:
        """Тест получения топ N вакансий"""
        top_2 = get_top_vacancies(sample_vacancies, 2)

        assert len(top_2) == 2
        assert top_2[0] == sample_vacancies[0]
        assert top_2[1] == sample_vacancies[1]

        top_10 = get_top_vacancies(sample_vacancies, 10)

        assert len(top_10) == 4

        top_0 = get_top_vacancies(sample_vacancies, 0)

        assert len(top_0) == 0

    def test_get_top_vacancies_negative(self, sample_vacancies: list[Vacancy]) -> None:
        """Тест получения отрицательного количества вакансий"""
        result = get_top_vacancies(sample_vacancies, -1)
        assert len(result) == 0

    def test_print_vacancies_empty(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест вывода пустого списка вакансий"""
        print_vacancies([])

        captured = capsys.readouterr()
        assert "Вакансии не найдены" in captured.out

    def test_print_vacancies_with_data(
        self, sample_vacancies: list[Vacancy], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест вывода вакансий"""
        print_vacancies(sample_vacancies[:2])

        captured = capsys.readouterr()

        assert "Python Developer" in captured.out
        assert "Java Developer" in captured.out
        assert "Всего найдено вакансий: 2" in captured.out
        assert "=" * 60 in captured.out

    def test_print_vacancies_format(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест формата вывода вакансий"""
        vacancy = Vacancy(
            name="Test Vacancy",
            url="https://test.com",
            salary="100000 руб.",
            description="Test description",
            company="Test Company",
            experience="1-3 года",
            employment="Полная занятость",
        )

        print_vacancies([vacancy])

        captured = capsys.readouterr()
        output = captured.out

        assert "Test Vacancy" in output
        assert "Test Company" in output
        assert "100000 руб." in output
        assert "1-3 года" in output
        assert "Полная занятость" in output
        assert "https://test.com" in output
        assert "Test description" in output
