import pandas as pd
import matplotlib.pyplot as plt
from models.database import Database

db = Database()

def visualize_grades():
    df = pd.read_sql_query("SELECT * FROM students", db.conn)

    if df.empty:
        print("No data available")
        return

    df["grade"].value_counts().plot(kind="bar")
    plt.title("Grade Distribution")
    plt.show()
