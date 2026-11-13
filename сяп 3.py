import json
import os
from datetime import datetime

def process_books_file(file_path="books.txt"):
    totalcount = 0
    invalidcount = 0
    author_books = {}


    oldest_book = None
    newest_book = None

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(";")
                if len(parts) != 4:
                    invalidcount += 1
                    continue

                author, title, year_str, count_str = [p.strip() for p in parts]

                try:
                    year = int(year_str)
                    count = int(count_str)
                    if not author or not title or count < 0:
                        invalidcount += 1
                        continue
                except ValueError:
                    invalidcount += 1
                    continue

                totalcount += count
                author_books[author] = author_books.get(author, 0) + count

                if oldest_book is None or year < oldest_book["year"]:
                    oldest_book = {
                        "author": author,
                        "title": title,
                        "year": year,
                        "count": count,
                    }
                if newest_book is None or year > newest_book["year"]:
                    newest_book = {
                        "author": author,
                        "title": title,
                        "year": year,
                        "count": count,
                    }

    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден!")
        return

    print("\n РЕЗУЛЬТАТЫ")
    print(f"Общее число книг (экземпляров): {totalcount}")
    print(f"Количество некорректных/пропущенных строк: {invalidcount}\n")

    if oldest_book:
        print(
            f"Самая старая книга: «{oldest_book['title']}» ({oldest_book['author']}, {oldest_book['year']} г.)"
        )
    if newest_book:
        print(
            f"Самая новая книга: «{newest_book['title']}» ({newest_book['author']}, {newest_book['year']} г.)"
        )
    print("\nСловарь {автор: количество книг}:")
    print(author_books)



def group_books_by_author(input_file="books.txt", output_file="by_author.txt"):
    authors_data = {}
    has_valid_data = False

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if not lines:
            print("ОШИБКА: Файл  'books.txt' абсолютно  пуст! ")
            return
        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split(";")
            if len(parts) != 4:
                continue

            author, title, year_str, count_str = [p.strip() for p in parts]

            try:
                year = int(year_str)
                count = int(count_str)
                if not author or not title or count < 0:
                    continue
            except ValueError:
                continue


            has_valid_data = True


            if author not in authors_data:
                authors_data[author] = []

            authors_data[author].append(
                {"title": title, "year": year, "count": count}
            )

        if not has_valid_data:
            print(
                "ОШИБКА: Файл не содержит ни одной корректной записи о книгах!"
            )
            return

        with open(output_file, "w", encoding="utf-8") as out_file:
            for author, books in authors_data.items():
                out_file.write(f"{author}\n")
                total_author_books = 0

                for book in books:

                    out_file.write(  f"    {book['title']} ({book['year']} г.) — {book['count']} шт.\n" )
                    total_author_books += book["count"]


                out_file.write(f"Итого книг автора: {total_author_books}\n\n")

        print(
            f"Успех! Данные сгруппированы и сохранены в файл '{output_file}'."
        )

    except FileNotFoundError:
        print(f"ОШИБКА: Входной файл '{input_file}' не найден!")


def save_books_to_json(input_file="books.txt", output_file="library.json"):
        books_list = []

        try:

            with open(input_file, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(";")
                    if len(parts) != 4:
                        continue

                    author, title, year_str, count_str = [p.strip() for p in parts]

                    try:
                        year = int(year_str)
                        count = int(count_str)
                        if not author or not title or count < 0:
                            continue
                    except ValueError:
                        continue

                    books_list.append({
                        "автор": author,
                        "название": title,
                        "год": year,
                        "количество": count
                    })

            current_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            final_data = {
                "обновлено": current_date,
                "всего": len(books_list),
                "книги": books_list
            }

            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(final_data, json_file, ensure_ascii=False, indent=4)

            print(f"Успех! Данные сохранены в формате JSON в файл '{output_file}'.")

        except FileNotFoundError:
            print(f"ОШИБКА: Файл '{input_file}' не найден!")



def search_books_in_json(input_file="library.json", output_file="search_results.json"):
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        books = data.get("книги", [])
        if not books:
            print("В файле нет списка книг для поиска.")
            return

    except FileNotFoundError:
        print(f"ОШИБКА: Файл '{input_file}' не найден! Сначала выполните задание 3.")
        return

    print("\n-ПОИСК КНИГ")
    print("(Оставьте поле пустым и нажмите Enter, если этот критерий не нужен)")
    search_author = input("Введите имя автора (или часть имени): ").strip().lower()
    search_title = input("Введите часть названия книги: ").strip().lower()
    year_min_str = input("Введите минимальный год: ").strip()
    year_max_str = input("Введите максимальный год: ").strip()
    
    year_min = int(year_min_str) if year_min_str.isdigit() else None
    year_max = int(year_max_str) if year_max_str.isdigit() else None

    found_books = []

    for book in books:
        try:

            author = book["автор"]
            title = book["название"]
            year = book["год"]
            match = True
            if search_author and search_author not in author.lower():
                match = False
            if search_title and search_title not in title.lower():
                match = False
            if year_min is not None and year < year_min:
                match = False
            if year_max is not None and year > year_max:
                match = False

            if match:
                found_books.append(book)

        except KeyError as e:
            print(f"Внимание: пропущена некорректная запись. Отсутствует ключ {e}")
            continue


    if found_books:
        with open(output_file, "w", encoding="utf-8") as out_file:
            json.dump(found_books, out_file, ensure_ascii=False, indent=4)
        print(f"\nПоиск завершен. Найдено книг: {len(found_books)}.")
        print(f"Результаты сохранены в файл '{output_file}'.")
    else:
        print("\nПо вашему запросу не найдено ни одной книги.")


DATA_FILE = 'library.json'
LOG_FILE = 'library_log.txt'

def log_operation(operation, status, details=""):
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {operation} - {status} - {details}\n")
    except Exception as e:
        print(f"Ошибка при записи в журнал: {e}")

def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            default_data = {
                "books": {
                    "1": {"title": "Мастер и Маргарита", "quantity": 5},
                    "2": {"title": "Преступление и наказание", "quantity": 2},
                    "3": {"title": "Евгений Онегин", "quantity": 0}
                },
                "debtors": {}
            }
            save_data(default_data)
            return default_data

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            log_operation("Загрузка данных", "Успешно")
            return data
    except Exception as e:
        log_operation("Загрузка данных", "Ошибка", str(e))
        print(f"Ошибка загрузки данных: {e}")
        return {"books": {}, "debtors": {}}


def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        log_operation("Сохранение данных", "Успешно")
    except Exception as e:
        log_operation("Сохранение данных", "Ошибка", str(e))
        print(f"Ошибка сохранения данных: {e}")



def issue_book(data):
    try:
        book_id = input("Введите ID книги (например, 1, 2 или 3): ").strip()
        reader_name = input("Введите имя читателя: ").strip()

        if book_id not in data['books']:
            print("Книга с таким ID не найдена.")
            log_operation("Выдача книги", "Неудачно", f"Книга {book_id} не найдена")
            return

        book = data['books'][book_id]

        if book['quantity'] <= 0:
            raise ValueError(f"Книги «{book['title']}» нет в наличии (остаток 0).")


        book['quantity'] -= 1

        if reader_name not in data['debtors']:
            data['debtors'][reader_name] = {}
        return_date = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')
        data['debtors'][reader_name][book_id] = return_date

        print(f"Книга «{book['title']}» успешно выдана читателю {reader_name}. Вернуть до: {return_date}")
        log_operation("Выдача книги", "Успешно", f"Книга: {book_id}, Читатель: {reader_name}")

    except ValueError as ve:

        print(f"ОШИБКА: {ve}")
        log_operation("Выдача книги", "Ошибка", str(ve))
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        log_operation("Выдача книги", "Ошибка", str(e))


def return_book(data):
    try:
        book_id = input("Введите ID книги: ").strip()
        reader_name = input("Введите имя читателя: ").strip()

        if reader_name not in data['debtors'] or book_id not in data['debtors'][reader_name]:
            print(f"За читателем {reader_name} не числится эта книга.")
            log_operation("Возврат книги", "Неудачно", f"Читатель: {reader_name}, Книга: {book_id} (не числится)")
            return

        if book_id in data['books']:
            data['books'][book_id]['quantity'] += 1
        else:
            print("Внимание: Данная книга была удалена из каталога, но сейчас возвращена.")

        del data['debtors'][reader_name][book_id]

        if not data['debtors'][reader_name]:
            del data['debtors'][reader_name]

        print("Книга успешно возвращена в библиотеку.")
        log_operation("Возврат книги", "Успешно", f"Книга: {book_id}, Читатель: {reader_name}")

    except Exception as e:
        print(f"Ошибка при возврате книги: {e}")
        log_operation("Возврат книги", "Ошибка", str(e))



def list_debtors(data):
    try:
        if not data['debtors']:
            print("Список должников пуст. Все книги в библиотеке.")
            log_operation("Просмотр списка должников", "Успешно", "Список пуст")
            return

        print("\n СПИСОК ДОЛЖНИКОВ ")
        for reader, books in data['debtors'].items():
            print(f"Читатель: {reader}")
            for book_id, return_date in books.items():
                title = data['books'].get(book_id, {}).get('title', 'Неизвестная книга')
                print(f"  - «{title}» (ID: {book_id}), вернуть до: {return_date}")
        print("------------------------")
        log_operation("Просмотр списка должников", "Успешно")
    except Exception as e:
        print(f"Ошибка при выводе списка должников: {e}")
        log_operation("Просмотр списка должников", "Ошибка", str(e))



def main_menu():
    data = load_data()

    while True:
        print("\n СИСТЕМА УЧЕТА БИБЛИОТЕКИ")
        print("1. Выдать книгу")
        print("2. Вернуть книгу")
        print("3. Список должников")
        print("4. Сохранить и выйти")

        choice = input("Выберите действие (1-4): ").strip()

        try:
            choice_num = int(choice)

            if choice_num == 1:
                issue_book(data)
            elif choice_num == 2:
                return_book(data)
            elif choice_num == 3:
                list_debtors(data)
            elif choice_num == 4:
                save_data(data)
                print("Данные сохранены. Работа завершена.")
                break
            else:
                print("Неверный выбор. Пожалуйста, введите номер от 1 до 4.")

        except ValueError:
            print("ОШИБКА: Пожалуйста, введите число (1-4), а не текст.")





user_input = input("Введите номер задания от 1 до 5 (выйти - 0): ")

if user_input.isdigit():
    number = int(user_input)
else:
    number = -1


if number == 1:
    data = """Булгаков;Мастер и Маргарита;1967;2
Толстой;Война и мир;1869;22
Толстой;Анна Каренина;1877;1
Достоевский;Преступление и наказание;1866;4
Некорректная_строка_без_разделителей
Чехов;Три сестры;не_число;1
;Без автора;2000;5
Пушкин;Евгений Онегин;1833;3"""


    with open("books.txt", "w", encoding="utf-8") as file:
        file.write(data)

    print("Файл books.txt успешно создан!")
    process_books_file("books.txt")

elif number == 2:
    group_books_by_author("books.txt", "by_author.txt")

elif number == 3:
    save_books_to_json("books.txt", "library.json")
elif number == 4:
    search_books_in_json("library.json", "search_results.json")
elif number == 5:
    main_menu()
elif number == 0:
    print("Выход из программы.")
else:
    print("Некорректный ввод!")