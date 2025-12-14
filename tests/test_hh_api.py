from typing import Any
from unittest.mock import Mock, patch

import pytest
import requests

from src.hh_api import HeadHunterAPI


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI"""

    def test_init(self) -> None:
        """Тест инициализации"""
        api = HeadHunterAPI()

        assert api.BASE_URL == "https://api.hh.ru/vacancies"
        assert "User-Agent" in api._session.headers

    @patch("requests.Session.get")
    def test_connect_success(self, mock_get: Mock) -> None:
        """Тест успешного подключения"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        api.connect()

    @patch("requests.Session.get")
    def test_connect_failure(self, mock_get: Mock, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест неудачного подключения"""
        mock_get.side_effect = requests.RequestException("Connection error")

        api = HeadHunterAPI()
        api.connect()

        captured = capsys.readouterr()
        assert "Ошибка подключения" in captured.out

    @patch.object(HeadHunterAPI, "connect")
    @patch("requests.Session.get")
    def test_get_vacancies(self, mock_get: Mock, mock_connect: Mock) -> None:
        """Тест получения вакансий"""
        mock_connect.return_value = None

        mock_response_main = Mock()
        mock_response_main.json.return_value = {
            "items": [
                {"id": "1", "url": "https://api.hh.ru/vacancies/1"},
                {"id": "2", "url": "https://api.hh.ru/vacancies/2"},
            ]
        }

        mock_response_detail = Mock()
        mock_response_detail.json.return_value = {
            "id": "1",
            "name": "Python Developer",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "description": "Test description",
            "employer": {"name": "Test Company"},
            "experience": {"name": "1-3 года"},
            "employment": {"name": "Полная занятость"},
            "schedule": {"name": "Полный день"},
            "published_at": "2024-01-01T00:00:00",
            "alternate_url": "https://hh.ru/vacancy/1",
            "snippet": {"requirement": "Python", "responsibility": "Разработка"},
        }

        mock_get.side_effect = [mock_response_main, mock_response_detail, mock_response_detail]

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        mock_connect.assert_called_once()

        assert len(vacancies) == 2
        assert vacancies[0]["name"] == "Python Developer"

    @patch.object(HeadHunterAPI, "connect")
    @patch("requests.Session.get")
    def test_get_vacancies_request_exception(
        self, mock_get: Mock, mock_connect: Mock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест исключения при запросе вакансий"""
        mock_connect.return_value = None
        mock_get.side_effect = requests.RequestException("API error")

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        assert vacancies == []

        captured = capsys.readouterr()
        assert "Ошибка при получении вакансий" in captured.out

    def test_format_vacancies(self) -> None:
        """Тест форматирования вакансий"""
        api = HeadHunterAPI()

        raw_vacancies: list[dict[str, Any]] = [
            {
                "id": "1",
                "name": "Python Developer",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "description": "<p>Test <b>description</b></p>",
                "employer": {"name": "Test Company"},
                "experience": {"name": "1-3 года"},
                "employment": {"name": "Полная занятость"},
                "schedule": {"name": "Полный день"},
                "published_at": "2024-01-01T00:00:00",
                "alternate_url": "https://hh.ru/vacancy/1",
                "snippet": {"requirement": "Python 3+", "responsibility": "Backend development"},
            },
            {
                "id": "2",
                "name": "Java Developer",
                "salary": None,
                "description": "No salary",
                "employer": {"name": "Company2"},
                "alternate_url": "https://hh.ru/vacancy/2",
            },
        ]

        formatted = api.format_vacancies(raw_vacancies)

        assert len(formatted) == 2

        assert formatted[0]["name"] == "Python Developer"
        assert formatted[0]["salary"] == "100000 - 150000 RUR"
        assert formatted[0]["salary_from"] == 100000
        assert formatted[0]["salary_to"] == 150000
        assert "Test description" in formatted[0]["description"]
        assert "Python 3+" in formatted[0]["requirements"]
        assert "Backend development" in formatted[0]["requirements"]
        assert formatted[0]["company"] == "Test Company"

        assert formatted[1]["salary"] == "Зарплата не указана"
        assert formatted[1]["salary_from"] is None
        assert formatted[1]["salary_to"] is None

    def test_clean_description(self) -> None:
        """Тест очистки HTML из описания"""
        api = HeadHunterAPI()

        html_text = "<p>This is <b>bold</b> and <i>italic</i> text.</p>"
        cleaned = api._clean_description(html_text)

        assert cleaned == "This is bold and italic text."
        assert "<" not in cleaned
        assert ">" not in cleaned

    def test_clean_description_none(self) -> None:
        """Тест очистки пустого описания"""
        api = HeadHunterAPI()

        result = api._clean_description(None)
        assert result == ""

        result = api._clean_description("")
        assert result == ""

    def test_get_requirements(self) -> None:
        """Тест извлечения требований"""
        api = HeadHunterAPI()

        vacancy1 = {"snippet": {"requirement": "Python experience", "responsibility": "Develop backend"}}

        requirements1 = api._get_requirements(vacancy1)
        assert "Python experience" in requirements1
        assert "Develop backend" in requirements1

        vacancy2 = {"snippet": {"requirement": "Java knowledge", "responsibility": None}}

        requirements2 = api._get_requirements(vacancy2)
        assert "Java knowledge" in requirements2

        vacancy3 = {"snippet": {"requirement": None, "responsibility": "Code review"}}

        requirements3 = api._get_requirements(vacancy3)
        assert "Code review" in requirements3

        vacancy4 = {"snippet": {}, "description": "Long description text here" * 10}

        requirements4 = api._get_requirements(vacancy4)
        assert "Long description text here" in requirements4
        assert "..." in requirements4

    @patch("requests.Session.get")
    def test_get_vacancy_details_success(self, mock_get: Mock) -> None:
        """Тест получения деталей вакансии"""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "1", "name": "Test"}
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        result = api._get_vacancy_details("https://api.hh.ru/vacancies/1")

        assert result == {"id": "1", "name": "Test"}

    @patch("requests.Session.get")
    def test_get_vacancy_details_failure(self, mock_get: Mock) -> None:
        """Тест ошибки при получении деталей вакансии"""
        mock_get.side_effect = requests.RequestException("Error")

        api = HeadHunterAPI()
        result = api._get_vacancy_details("https://api.hh.ru/vacancies/1")

        assert result is None
