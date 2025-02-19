import sqlite3

def add_columns_to_tables(db_name):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()


        cursor.execute("PRAGMA table_info(Преподаватель);")
        columns = [column[1] for column in cursor.fetchall()]
        if "Email" not in columns:
            cursor.execute("""
                ALTER TABLE Преподаватель
                ADD COLUMN Email TEXT;
            """)
            print("Колонка 'Email' успешно добавлена в таблицу 'Преподаватель'.")
        else:
            print("Колонка 'Email' уже существует в таблице 'Преподаватель'.")

        if "Телефон" not in columns:
            cursor.execute("""
                ALTER TABLE Преподаватель
                ADD COLUMN Телефон TEXT;
            """)
            print("Колонка 'Телефон' успешно добавлена в таблицу 'Преподаватель'.")
        else:
            print("Колонка 'Телефон' уже существует в таблице 'Преподаватель'.")


        cursor.execute("PRAGMA table_info(Пара);")
        columns = [column[1] for column in cursor.fetchall()]
        if "Описание" not in columns:
            cursor.execute("""
                ALTER TABLE Пара
                ADD COLUMN Описание TEXT;
            """)
            print("Колонка 'Описание' успешно добавлена в таблицу 'Пара'.")
        else:
            print("Колонка 'Описание' уже существует в таблице 'Пара'.")

        connection.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении новых колонок: {e}")
    finally:
        if connection:
            connection.close()


def create_indexes(db_name):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()


        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_Преподаватель_Должность
            ON Преподаватель (Должность);
        """)
        print("Индекс 'idx_Преподаватель_Должность' успешно создан или уже существует.")


        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_Пара_Вид_занятия
            ON Пара (Вид_занятия);
        """)
        print("Индекс 'idx_Пара_Вид_занятия' успешно создан или уже существует.")

        connection.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при создании индексов: {e}")
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    DATABASE_NAME = "university.db"


    add_columns_to_tables(DATABASE_NAME)
    create_indexes(DATABASE_NAME)
