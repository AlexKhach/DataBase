import sqlite3

def initialize_database(db_name):
    try:

        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Преподаватель (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ФИО TEXT NOT NULL,
                Кафедра TEXT NOT NULL,
                Должность TEXT NOT NULL,
                Уч_степень TEXT NOT NULL
            );
        """)


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Пара (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Дата TEXT NOT NULL,
                Время TEXT NOT NULL,
                Аудитория TEXT NOT NULL,
                Вид_занятия TEXT NOT NULL,
                Группа TEXT NOT NULL,
                преподаватель_id INTEGER NOT NULL,
                предмет_id INTEGER NOT NULL,
                FOREIGN KEY (преподаватель_id) REFERENCES Преподаватель (id),
                FOREIGN KEY (предмет_id) REFERENCES Предмет (id)
            );
        """)


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Предмет (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Название TEXT NOT NULL,
                Обязательность TEXT NOT NULL,
                Вид_проверки TEXT NOT NULL,
                Число_часов INTEGER NOT NULL
            );
        """)

        connection.commit()
        print(f"База данных '{db_name}' успешно создана и инициализирована.")

    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:

        if connection:
            connection.close()

if __name__ == "__main__":
    DATABASE_NAME = "university.db"

    initialize_database(DATABASE_NAME)
