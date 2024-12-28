import sqlite3

def initialize_database(db_name):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # Create Преподаватель table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Преподаватель (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ФИО TEXT NOT NULL,
                Кафедра TEXT NOT NULL,
                Должность TEXT NOT NULL,
                Уч_степень TEXT NOT NULL
            );
        """)

        # Create Предмет table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Предмет (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Название TEXT NOT NULL,
                Обязательность TEXT NOT NULL,
                Вид_проверки TEXT NOT NULL,
                Число_часов INTEGER NOT NULL
            );
        """)

        # Create Пара table with DATE and TIME types for Дата and Время columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Пара (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Дата TEXT NOT NULL,  -- This will store the date in TEXT, in ISO format YYYY-MM-DD
                Время TEXT NOT NULL, -- This will store the time in TEXT, in ISO format HH:MM:SS
                Аудитория TEXT NOT NULL,
                Вид_занятия TEXT NOT NULL,
                Группа TEXT NOT NULL,
                преподаватель_id INTEGER NOT NULL,
                предмет_id INTEGER NOT NULL,
                FOREIGN KEY (преподаватель_id) REFERENCES Преподаватель (id),
                FOREIGN KEY (предмет_id) REFERENCES Предмет (id)
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
