from fastapi import FastAPI
from routes import auth_routes, student_routes

app = FastAPI(
    title="Final Year Student Result Management System",
    version="3.0"
)

app.include_router(auth_routes.router)
app.include_router(student_routes.router)
