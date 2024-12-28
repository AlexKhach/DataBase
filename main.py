from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3


app = FastAPI()


DATABASE_NAME = "university.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


class Teacher(BaseModel):
    ФИО: str
    Кафедра: str
    Должность: str
    Уч_степень: str

class TeacherResponse(Teacher):
    id: int


@app.get("/")
def read_root():
    return {"message": "Welcome to the University API!"}


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
    cursor = conn.cursor()
    teachers = cursor.execute("SELECT * FROM Преподаватель").fetchall()
    conn.close()
    return [dict(teacher) for teacher in teachers]

@app.get("/teachers/{id}", response_model=TeacherResponse)
def read_teacher(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    teacher = cursor.execute("SELECT * FROM Преподаватель WHERE id = ?", (id,)).fetchone()
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
