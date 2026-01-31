import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import hashlib

def get_connection():
    return sqlite3.connect("students.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            math INTEGER,
            science INTEGER,
            english INTEGER,
            total INTEGER,
            average REAL,
            grade TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

def calculate_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"


def add_student(name, math, science, english):
    total = math + science + english
    average = total / 3
    grade = calculate_grade(average)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (name, math, science, english, total, average, grade)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, math, science, english, total, average, grade))

    conn.commit()
    conn.close()

def fetch_students():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    return df

st.set_page_config(page_title="Student Result System", layout="wide")

create_tables()

# Create default admin if not exists
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE username='admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   ("admin", hash_password("admin123"), "admin"))
    conn.commit()
conn.close()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    st.title("🎓 Student Result Management System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.role = user[3]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

else:

    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to", ["Add Student", "View Students", "Analytics", "Logout"])

    if menu == "Add Student":

        st.header("Add New Student")

        name = st.text_input("Student Name")
        math = st.number_input("Math Marks", 0, 100)
        science = st.number_input("Science Marks", 0, 100)
        english = st.number_input("English Marks", 0, 100)

        if st.button("Add Student"):
            try:
                add_student(name, math, science, english)
                st.success("Student added successfully!")
            except Exception as e:
                st.error(f"Error: {e}")


    elif menu == "View Students":

        st.header("Student Records")

        df = fetch_students()
        st.dataframe(df)

        search = st.text_input("Search Student")

        if search:
            filtered = df[df["name"].str.contains(search, case=False)]
            st.dataframe(filtered)


    elif menu == "Analytics":

        st.header("Performance Analytics")

        df = fetch_students()

        if not df.empty:
            fig, ax = plt.subplots()
            ax.bar(df["name"], df["average"])
            ax.set_ylabel("Average Marks")
            ax.set_title("Student Performance")

            st.pyplot(fig)
        else:
            st.warning("No data available")


    elif menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()