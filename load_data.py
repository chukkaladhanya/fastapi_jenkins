import pandas as pd
from sqlalchemy import create_engine

def load_data():
    df = pd.read_csv("student_data.csv")
    engine = create_engine("sqlite:///database.db")
    df.to_sql("students",engine,if_exists="replace",index=False)

    print("data loaded sucessfully into database from csv file")


