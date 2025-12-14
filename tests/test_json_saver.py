import json
import os
import tempfile
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.json_saver import JSONSaver
from src.vacancy import Vacancy


class TestJSONSaver:
    """Тесты для класса JSONSaver"""

    @pytest.fixture
    def temp_file(self) -> Any:
        """Создание временного файла для тестов"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            yield f.name
        os.unlink(f.name)

    @pytest.fixture
    def sample_vacancy(self) -> Vacancy:
        """Создание тестовой вакансии"""
        return Vacancy(
            name="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary="150000 - 200000 руб.",
            description="Разработка на Python",
            company="Yandex",
        )

    def test_init_creates_directory(self, tmp_path: Any) -> None:
        """Тест создания директории при инициализации"""
        temp_dir = tmp_path / "data"
        filename = temp_dir / "vacancies.json"
        saver = JSONSaver(str(filename))
        assert temp_dir.exists()

    def test_init_with_file_in_current_dir(self) -> None:
        """Тест инициализации с файлом в текущей директории"""
        saver = JSONSaver("test_vacancies.json")
        assert saver.filename == "test_vacancies.json"

    def test_add_vacancy(self, temp_file: str, sample_vacancy: Vacancy) -> None:
        """Тест добавления вакансии"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)

        with open(temp_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["name"] == "Python Developer"
        assert data[0]["url"] == "https://hh.ru/vacancy/123"

    def test_add_duplicate_vacancy(self, temp_file: str, sample_vacancy: Vacancy) -> None:
        """Тест добавления дубликата вакансии"""
        saver = JSONSaver(temp_file)

        saver.add_vacancy(sample_vacancy)
        saver.add_vacancy(sample_vacancy)

        with open(temp_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1

    def test_get_vacancies_empty_file(self, temp_file: str) -> None:
        """Тест получения вакансий из пустого файла"""
        saver = JSONSaver(temp_file)
        vacancies = saver.get_vacancies()

        assert vacancies == []

    def test_get_vacancies_with_data(self, temp_file: str, sample_vacancy: Vacancy) -> None:
        """Тест получения вакансий с данными"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)
        vacancies = saver.get_vacancies()

        assert len(vacancies) == 1
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0].name == "Python Developer"

    def test_get_vacancies_with_criteria(self, temp_file: str) -> None:
        """Тест получения вакансий с критериями"""
        saver = JSONSaver(temp_file)

        vacancies_data = [
            Vacancy("Python Developer", "url1", "100000 - 150000 руб.", "Python разработка", "Company1"),
            Vacancy("Java Developer", "url2", "80000 - 120000 руб.", "Java разработка", "Company2"),
            Vacancy("Senior Python", "url3", "200000 - 300000 руб.", "Python senior", "Company1"),
        ]

        for vacancy in vacancies_data:
            saver.add_vacancy(vacancy)

        python_vacancies = saver.get_vacancies({"keyword": "python"})
        assert len(python_vacancies) == 2

        high_salary_vacancies = saver.get_vacancies({"min_salary": 150000})
        assert len(high_salary_vacancies) == 1
        assert "Senior" in high_salary_vacancies[0].name

        company1_vacancies = saver.get_vacancies({"company": "company1"})
        assert len(company1_vacancies) == 2

        combined = saver.get_vacancies({"keyword": "python", "min_salary": 120000})
        assert len(combined) == 1

    def test_delete_vacancy(self, temp_file: str, sample_vacancy: Vacancy) -> None:
        """Тест удаления вакансии"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)
        vacancies = saver.get_vacancies()
        assert len(vacancies) == 1

        saver.delete_vacancy(sample_vacancy)
        vacancies = saver.get_vacancies()
        assert len(vacancies) == 0

    def test_delete_nonexistent_vacancy(self, temp_file: str, sample_vacancy: Vacancy) -> None:
        """Тест удаления несуществующей вакансии"""
        saver = JSONSaver(temp_file)
        saver.delete_vacancy(sample_vacancy)
        vacancies = saver.get_vacancies()
        assert len(vacancies) == 0

    def test_clear(self, temp_file: str) -> None:
        """Тест очистки всех вакансий"""
        saver = JSONSaver(temp_file)

        for i in range(3):
            vacancy = Vacancy(
                name=f"Job {i}",
                url=f"https://hh.ru/vacancy/{i}",
                salary=f"{i}00000 руб.",
                description=f"Description {i}",
                company=f"Company {i}",
            )
            saver.add_vacancy(vacancy)

        vacancies = saver.get_vacancies()
        assert len(vacancies) == 3

        saver.clear()
        vacancies = saver.get_vacancies()
        assert len(vacancies) == 0

    def test_filter_by_salary(self, temp_file: str) -> None:
        """Тест фильтрации по зарплате"""
        saver = JSONSaver(temp_file)

        vacancies_data = [
            Vacancy("Low", "url1", "50000 - 70000 руб.", "Desc1", "C1"),
            Vacancy("Medium", "url2", "80000 - 120000 руб.", "Desc2", "C2"),
            Vacancy("High", "url3", "150000 - 200000 руб.", "Desc3", "C3"),
        ]

        for vacancy in vacancies_data:
            saver.add_vacancy(vacancy)

        filtered = saver.filter_by_salary(min_salary=100000)
        assert len(filtered) == 1
        assert filtered[0].name == "High"

    def test_sort_by_salary(self, temp_file: str) -> None:
        """Тест сортировки по зарплате"""
        saver = JSONSaver(temp_file)

        vacancies_data = [
            Vacancy("Low", "url1", "50000 - 70000 руб.", "Desc1", "C1"),
            Vacancy("High", "url3", "150000 - 200000 руб.", "Desc3", "C3"),
            Vacancy("Medium", "url2", "80000 - 120000 руб.", "Desc2", "C2"),
        ]

        for vacancy in vacancies_data:
            saver.add_vacancy(vacancy)

        sorted_desc = saver.sort_by_salary(descending=True)
        assert sorted_desc[0].name == "High"
        assert sorted_desc[1].name == "Medium"
        assert sorted_desc[2].name == "Low"

        sorted_asc = saver.sort_by_salary(descending=False)
        assert sorted_asc[0].name == "Low"
        assert sorted_asc[2].name == "High"

    @patch("os.makedirs")
    @patch("builtins.open")
    def test_load_vacancies_file_not_found(self, mock_open: MagicMock, _: MagicMock) -> None:
        """Тест загрузки при отсутствии файла"""
        mock_open.side_effect = FileNotFoundError()

        saver = JSONSaver("nonexistent.json")
        vacancies = saver._load_vacancies()
        assert vacancies == []

    @patch("os.makedirs")
    @patch("json.load")
    @patch("builtins.open")
    def test_load_vacancies_json_decode_error(
        self, mock_open: MagicMock, mock_json_load: MagicMock, _: MagicMock
    ) -> None:
        """Тест загрузки при ошибке JSON"""
        mock_file_obj = MagicMock()
        mock_file_obj.__enter__.return_value = mock_file_obj
        mock_file_obj.__exit__.return_value = None
        mock_open.return_value = mock_file_obj

        mock_json_load.side_effect = json.JSONDecodeError("Error", "", 0)

        saver = JSONSaver("invalid.json")
        vacancies = saver._load_vacancies()
        assert vacancies == []

    def test_save_vacancies_creates_file(self, tmp_path: Any) -> None:
        """Тест сохранения вакансий с созданием файла"""
        temp_file = tmp_path / "data" / "vacancies.json"
        saver = JSONSaver(str(temp_file))

        vacancy = Vacancy("Test", "url", "100000 руб.", "Test description", "Test Company")
        saver.add_vacancy(vacancy)

        assert temp_file.exists()

        with open(temp_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["name"] == "Test"
