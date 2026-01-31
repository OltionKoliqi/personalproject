from models.database import Database
from utils.auth_utils import hash_password, create_access_token

db = Database()

def register_service(user):
    try:
        hashed = hash_password(user.password)
        db.cursor.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            (user.username, hashed, user.role)
        )
        db.conn.commit()
        return {"message": "User registered successfully"}
    except:
        return {"error": "User already exists"}

def login_service(user):
    hashed = hash_password(user.password)
    db.cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (user.username, hashed)
    )
    result = db.cursor.fetchone()

    if result:
        token = create_access_token({
            "username": user.username,
            "role": result[0]
        })
        return {"access_token": token}

    return {"error": "Invalid credentials"}
