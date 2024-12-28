import requests
import random
from datetime import date, time

# Base URL of your API
BASE_URL = "http://127.0.0.1:8000"

# Function to generate random data for a teacher
def generate_teacher_data():
    first_names = ["Иван", "Сергей", "Дмитрий", "Алексей", "Андрей"]
    last_names = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов"]
    patronymics = ["Иванович", "Сергеевич", "Алексеевич", "Павлович", "Андреевич"]
    departments = ["Математика", "Физика", "Химия", "Биология", "Информатика"]
    positions = ["Профессор", "Доцент", "Старший преподаватель", "Ассистент"]
    degrees = ["Доктор наук", "Кандидат наук", "Магистр"]

    return {
        "ФИО": f"{random.choice(last_names)} {random.choice(first_names)} {random.choice(patronymics)}",
        "Кафедра": random.choice(departments),
        "Должность": random.choice(positions),
        "Уч_степень": random.choice(degrees)
    }

# Function to generate random data for a subject
def generate_subject_data():
    subjects = ["Математика", "Физика", "Химия", "Биология", "Информатика"]
    types = ["Обязательный", "Выборочный"]
    exam_types = ["Экзамен", "Зачет", "Контрольная работа"]
    hours = [30, 40, 50, 60]

    return {
        "Название": random.choice(subjects),
        "Обязательность": random.choice(types),
        "Вид_проверки": random.choice(exam_types),
        "Число_часов": random.choice(hours)
    }

# Function to generate random data for a class
def generate_class_data(teachers, subjects):
    class_date = date.today().strftime('%Y-%m-%d')  # Convert date to string
    class_time = time(random.randint(8, 18), random.randint(0, 59)).strftime('%H:%M:%S')  # Convert time to string
    classrooms = ["101", "102", "103", "104", "201", "202"]
    types_of_classes = ["Лекция", "Практика", "Семинар"]
    groups = ["Группа 1", "Группа 2", "Группа 3", "Группа 4"]

    return {
        "Дата": class_date,  # String format: 'YYYY-MM-DD'
        "Время": class_time,  # String format: 'HH:MM:SS'
        "Аудитория": random.choice(classrooms),
        "Вид_занятия": random.choice(types_of_classes),
        "Группа": random.choice(groups),
        "преподаватель_id": random.choice(teachers)["id"],
        "предмет_id": random.choice(subjects)["id"]
    }

# Function to create a teacher via API
def create_teacher(data):
    response = requests.post(f"{BASE_URL}/teachers/", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при добавлении преподавателя: {response.status_code}, {response.text}")
        return None

# Function to create a subject via API
def create_subject(data):
    response = requests.post(f"{BASE_URL}/subjects/", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при добавлении предмета: {response.status_code}, {response.text}")
        return None

# Function to create a class via API
def create_class(data):
    response = requests.post(f"{BASE_URL}/classes/", json=data)
    if response.status_code == 200:
        print(f"Успешно добавлено занятие: {data['Дата']} {data['Время']} - {data['Аудитория']}")
    else:
        print(f"Ошибка при добавлении занятия: {response.status_code}, {response.text}")

# Main logic to populate the database
def populate_data(num_teachers, num_subjects, num_classes):
    teachers = [create_teacher(generate_teacher_data()) for _ in range(num_teachers)]
    subjects = [create_subject(generate_subject_data()) for _ in range(num_subjects)]

    # Filter out None values in case of failed creations
    teachers = [teacher for teacher in teachers if teacher is not None]
    subjects = [subject for subject in subjects if subject is not None]

    for _ in range(num_classes):
        class_data = generate_class_data(teachers, subjects)
        create_class(class_data)

if __name__ == "__main__":
    num_teachers = 100  # Number of teachers
    num_subjects = 50   # Number of subjects
    num_classes = 200   # Number of classes

    populate_data(num_teachers, num_subjects, num_classes)
