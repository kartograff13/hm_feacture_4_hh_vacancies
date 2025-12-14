from typing import Any

from src import (HeadHunterAPI, JSONSaver, Vacancy, filter_vacancies, get_top_vacancies, get_vacancies_by_salary,
                 print_vacancies, sort_vacancies)


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем"""
    print("=" * 60)
    print("ПАРСЕР ВАКАНСИЙ С HH.RU")
    print("=" * 60)

    hh_api = HeadHunterAPI()
    hh_api.connect()

    json_saver = JSONSaver()

    while True:
        print("\nМеню:")
        print("1. Поиск вакансий")
        print("2. Показать сохраненные вакансии")
        print("3. Фильтровать сохраненные вакансии")
        print("4. Очистить сохраненные вакансии")
        print("5. Выход")

        choice = input("\nВыберите действие (1-5): ").strip()

        if choice == "1":
            search_vacancies(hh_api, json_saver)
        elif choice == "2":
            show_saved_vacancies(json_saver)
        elif choice == "3":
            filter_saved_vacancies(json_saver)
        elif choice == "4":
            json_saver.clear()
            print("Сохраненные вакансии очищены.")
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")


def search_vacancies(hh_api: HeadHunterAPI, json_saver: JSONSaver) -> None:
    """Поиск вакансий по запросу"""
    search_query = input("Введите поисковый запрос (например: Python разработчик): ").strip()

    if not search_query:
        print("Поисковый запрос не может быть пустым")
        return

    print("\nИдет поиск вакансий...")
    vacancies_data = hh_api.get_vacancies(search_query)

    if not vacancies_data:
        print("Вакансии не найдены.")
        return

    vacancies_list = Vacancy.cast_to_object_list(vacancies_data)

    print(f"\nНайдено {len(vacancies_list)} вакансий.")

    top_n_input = input("\nВведите количество вакансий для вывода в топ N: ").strip()
    try:
        top_n = int(top_n_input) if top_n_input else 10
    except ValueError:
        print("Неверный формат числа. Будет использовано значение по умолчанию: 10")
        top_n = 10

    filter_words_input = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").strip()
    filter_words = filter_words_input.split() if filter_words_input else []

    salary_range = input("Введите диапазон зарплат (например: 50000-150000): ").strip()

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print_vacancies(top_vacancies)

    save_choice = input("\nСохранить результаты в файл? (y/n): ").strip().lower()
    if save_choice == "y":
        for vacancy in top_vacancies:
            json_saver.add_vacancy(vacancy)
        print(f"Сохранено {len(top_vacancies)} вакансий.")


def show_saved_vacancies(json_saver: JSONSaver) -> None:
    """Показать сохраненные вакансии"""
    vacancies = json_saver.get_vacancies()

    if not vacancies:
        print("Сохраненных вакансий нет.")
        return

    print(f"\nСохранено {len(vacancies)} вакансий.")

    top_n_input = input("Сколько вакансий показать? (введите число или 'all' для всех): ").strip() or "10"

    if top_n_input.lower() == "all":
        top_n = len(vacancies)
    else:
        try:
            top_n = int(top_n_input)
        except ValueError:
            print("Неверный формат числа. Будет показано 10 вакансий.")
            top_n = 10

    sorted_vacancies = sort_vacancies(vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print_vacancies(top_vacancies)


def filter_saved_vacancies(json_saver: JSONSaver) -> None:
    """Фильтрация сохраненных вакансий"""
    print("\nКритерии фильтрации:")
    print("1. По ключевому слову")
    print("2. По минимальной зарплате")
    print("3. По компании")
    print("4. Комбинированный фильтр")

    choice = input("\nВыберите тип фильтра (1-4): ").strip()

    criteria: dict[str, Any] = {}

    if choice == "1":
        keyword = input("Введите ключевое слово: ").strip()
        criteria["keyword"] = keyword
    elif choice == "2":
        try:
            min_salary = int(input("Введите минимальную зарплату: ").strip())
            criteria["min_salary"] = min_salary
        except ValueError:
            print("Неверный формат зарплаты.")
            return
    elif choice == "3":
        company = input("Введите название компании: ").strip()
        criteria["company"] = company
    elif choice == "4":
        keyword = input("Введите ключевое слово (оставьте пустым, если не нужно): ").strip()
        if keyword:
            criteria["keyword"] = keyword

        min_salary_input = input("Введите минимальную зарплату (оставьте пустым, если не нужно): ").strip()
        if min_salary_input:
            try:
                criteria["min_salary"] = int(min_salary_input)
            except ValueError:
                print("Неверный формат зарплаты.")
                return
    else:
        print("Неверный выбор.")
        return

    vacancies = json_saver.get_vacancies(criteria)

    if not vacancies:
        print("Вакансии не найдены по заданным критериям.")
        return

    print(f"\nНайдено {len(vacancies)} вакансий.")
    top_n_input = input("Сколько вакансий показать? (введите число): ").strip() or "10"

    try:
        top_n = int(top_n_input)
    except ValueError:
        print("Неверный формат числа. Будет показано 10 вакансий.")
        top_n = 10

    sorted_vacancies = sort_vacancies(vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
