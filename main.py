from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date, time
import sqlite3
from sqlite3 import Error
app = FastAPI()

DATABASE_NAME = "university.db"

# Function to get database connection
def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row  # This allows column access by name (as dictionaries)
        return conn
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

# Models for Pydantic
class Teacher(BaseModel):
    ФИО: str
    Кафедра: str
    Должность: str
    Уч_степень: str

class TeacherResponse(Teacher):
    id: int

class Subject(BaseModel):
    Название: str
    Обязательность: str
    Вид_проверки: str
    Число_часов: int

class SubjectResponse(Subject):
    id: int

class Class(BaseModel):
    Дата: date
    Время: time
    Аудитория: str
    Вид_занятия: str
    Группа: str
    преподаватель_id: int
    предмет_id: int

class ClassResponse(Class):
    id: int

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the University API!"}

# CRUD for Teachers
@app.post("/teachers/", response_model=TeacherResponse)
def create_teacher(teacher: Teacher):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Преподаватель (ФИО, Кафедра, Должность, Уч_степень)
        VALUES (?, ?, ?, ?)
    """, (teacher.ФИО, teacher.Кафедра, teacher.Должность, teacher.Уч_степень))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {**teacher.dict(), "id": new_id}

@app.get("/teachers/", response_model=List[TeacherResponse])
def read_teachers():
    conn = get_db_connection()
    teachers = conn.execute("SELECT * FROM Преподаватель").fetchall()
    conn.close()
    return [dict(teacher) for teacher in teachers]

@app.get("/teachers/{id}", response_model=TeacherResponse)
def read_teacher(id: int):
    conn = get_db_connection()
    teacher = conn.execute("SELECT * FROM Преподаватель WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return dict(teacher)

@app.put("/teachers/{id}", response_model=TeacherResponse)
def update_teacher(id: int, teacher: Teacher):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Преподаватель
        SET ФИО = ?, Кафедра = ?, Должность = ?, Уч_степень = ?
        WHERE id = ?
    """, (teacher.ФИО, teacher.Кафедра, teacher.Должность, teacher.Уч_степень, id))
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {**teacher.dict(), "id": id}

@app.delete("/teachers/{id}")
def delete_teacher(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Преподаватель WHERE id = ?", (id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Teacher deleted successfully"}

# CRUD for Subjects
@app.post("/subjects/", response_model=SubjectResponse)
def create_subject(subject: Subject):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Предмет (Название, Обязательность, Вид_проверки, Число_часов)
        VALUES (?, ?, ?, ?)
    """, (subject.Название, subject.Обязательность, subject.Вид_проверки, subject.Число_часов))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {**subject.dict(), "id": new_id}

@app.get("/subjects/", response_model=List[SubjectResponse])
def read_subjects():
    conn = get_db_connection()
    subjects = conn.execute("SELECT * FROM Предмет").fetchall()
    conn.close()
    return [dict(subject) for subject in subjects]

@app.get("/subjects/{id}", response_model=SubjectResponse)
def read_subject(id: int):
    conn = get_db_connection()
    subject = conn.execute("SELECT * FROM Предмет WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return dict(subject)

@app.put("/subjects/{id}", response_model=SubjectResponse)
def update_subject(id: int, subject: Subject):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Предмет
        SET Название = ?, Обязательность = ?, Вид_проверки = ?, Число_часов = ?
        WHERE id = ?
    """, (subject.Название, subject.Обязательность, subject.Вид_проверки, subject.Число_часов, id))
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {**subject.dict(), "id": id}

@app.delete("/subjects/{id}")
def delete_subject(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Предмет WHERE id = ?", (id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Subject deleted successfully"}

# CRUD for Classes
@app.post("/classes/", response_model=ClassResponse)
def create_class(class_: Class):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Пара (Дата, Время, Аудитория, Вид_занятия, Группа, преподаватель_id, предмет_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (class_.Дата, class_.Время, class_.Аудитория, class_.Вид_занятия, class_.Группа, class_.преподаватель_id, class_.предмет_id))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {**class_.dict(), "id": new_id}

@app.get("/classes/", response_model=List[ClassResponse])
def read_classes():
    conn = get_db_connection()
    classes = conn.execute("SELECT * FROM Пара").fetchall()
    conn.close()
    return [dict(class_) for class_ in classes]

@app.get("/classes/{id}", response_model=ClassResponse)
def read_class(id: int):
    conn = get_db_connection()
    class_ = conn.execute("SELECT * FROM Пара WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return dict(class_)

@app.put("/classes/{id}", response_model=ClassResponse)
def update_class(id: int, class_: Class):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Пара
        SET Дата = ?, Время = ?, Аудитория = ?, Вид_занятия = ?, Группа = ?, преподаватель_id = ?, предмет_id = ?
        WHERE id = ?
    """, (class_.Дата, class_.Время, class_.Аудитория, class_.Вид_занятия, class_.Группа, class_.преподаватель_id, class_.предмет_id, id))
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Class not found")
    return {**class_.dict(), "id": id}

@app.delete("/classes/{id}")
def delete_class(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Пара WHERE id = ?", (id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Class not found")
    return {"message": "Class deleted successfully"}
