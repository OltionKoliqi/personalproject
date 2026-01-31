from fastapi import APIRouter
from models.user_model import UserCreate
from services.auth_services import register_service, login_service

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    return register_service(user)

@router.post("/login")
def login(user: UserCreate):
    return login_service(user)
