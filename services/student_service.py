from models.database import Database
from student_result_system.report_generator import calculate_grade
from utils.logger import log_info, log_error
import pandas as pd

db = Database()

async def add_student_service(student):
    try:
        total = student.math + student.science + student.english
        average = total / 3
        grade = calculate_grade(average)

        db.cursor.execute("""
        INSERT INTO students(name, math, science, english, total, average, grade)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (student.name, student.math, student.science,
              student.english, total, average, grade))

        db.conn.commit()
        log_info(f"Student {student.name} added")

        return {
            "name": student.name,
            "total": total,
            "average": average,
            "grade": grade
        }

    except Exception as e:
        log_error(str(e))
        return {"error": str(e)}

def get_students_service():
    db.cursor.execute("SELECT * FROM students")
    return db.cursor.fetchall()

def export_students_csv():
    db.cursor.execute("SELECT * FROM students")
    data = db.cursor.fetchall()

    df = pd.DataFrame(data, columns=[
        "ID","Name","Math","Science","English","Total","Average","Grade"
    ])

    file_path = "students_export.csv"
    df.to_csv(file_path, index=False)

    return {"file_saved_as": file_path}
