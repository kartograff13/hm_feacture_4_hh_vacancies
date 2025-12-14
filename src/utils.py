from src.vacancy import Vacancy


def filter_vacancies(vacancies: list[Vacancy], filter_words: list[str]) -> list[Vacancy]:
    """
    Фильтрация вакансий по ключевым словам.

    Args:
        vacancies: Список вакансий
        filter_words: Список ключевых слов

    Returns:
        Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        vacancy_text = f"{vacancy.name} {vacancy.description} {vacancy.company}".lower()
        if any(word.lower() in vacancy_text for word in filter_words):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies: list[Vacancy], salary_range: str) -> list[Vacancy]:
    """
    Фильтрация вакансий по диапазону зарплат.

    Args:
        vacancies: Список вакансий
        salary_range: Диапазон зарплат (формат: "100000-150000")

    Returns:
        Отфильтрованный список вакансий
    """
    if not salary_range or "-" not in salary_range:
        return vacancies

    try:
        min_salary, max_salary = map(int, salary_range.split("-"))

        filtered = []
        for vacancy in vacancies:
            if vacancy.salary_from and vacancy.salary_to:
                if not (vacancy.salary_to < min_salary or vacancy.salary_from > max_salary):
                    filtered.append(vacancy)
            elif vacancy.salary_from and vacancy.salary_from >= min_salary:
                filtered.append(vacancy)
            elif vacancy.salary_to and vacancy.salary_to <= max_salary:
                filtered.append(vacancy)

        return filtered
    except ValueError:
        return vacancies


def sort_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    """
    Сортировка вакансий по зарплате (по убыванию).

    Args:
        vacancies: Список вакансий

    Returns:
        Отсортированный список вакансий
    """
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: list[Vacancy], top_n: int) -> list[Vacancy]:
    """
    Получение топ N вакансий.

    Args:
        vacancies: Список вакансий
        top_n: Количество вакансий для вывода

    Returns:
        Список из top_n вакансий
    """
    return vacancies[:top_n]


def print_vacancies(vacancies: list[Vacancy]) -> None:
    """
    Вывод вакансий в консоль.

    Args:
        vacancies: Список вакансий для вывода
    """
    if not vacancies:
        print("Вакансии не найдены.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{'=' * 60}")
        print(f"Вакансия #{i}")
        print(f"{'=' * 60}")
        print(vacancy)

    print(f"\nВсего найдено вакансий: {len(vacancies)}")
