from fastapi import APIRouter, Depends
from models.student_model import StudentCreate
from services.student_service import add_student_service, get_students_service, export_students_csv
from utils.dependencies import role_required

router = APIRouter()

@router.post("/add-student")
async def add_student(
    student: StudentCreate,
    user=Depends(role_required("admin"))
):
    return await add_student_service(student)

@router.get("/students")
def get_students(user=Depends(role_required("admin"))):
    return get_students_service()

@router.get("/export")
def export(user=Depends(role_required("admin"))):
    return export_students_csv()
