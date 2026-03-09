from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException,status
from load_data import load_data
import sqlite3

load_data()
app = FastAPI()    


@app.get("/")

def redirect():
    return RedirectResponse(url="/details")


@app.get("/details")

def get_dataset_details():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students LIMIT 5")
    rows = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    conn.close()
    return {
        "status":"success",
        "status_code":status.HTTP_200_OK,
        "message":"Sample view of dataset",
        "count":count,
        "data":rows
        }


@app.get("/{gender}")

def get_female_students(gender : str):
    if(gender.lower() != "female" and gender.lower() != "male"):
        raise HTTPException(
        status_code=400,
        detail={
            "status": "error", 
            "message": "gender is invalid, only female and male are allowed"
            }       
    )

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    if(gender.lower()=="female"):
        cursor.execute("SELECT * FROM students WHERE SEX='F'")
    elif(gender.lower()=="male"):
        cursor.execute("SELECT * FROM students WHERE SEX='M'")

    rows = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM students WHERE SEX = 'F'")
    count = cursor.fetchone()[0]
    conn.close()
    return {
        "status":"success",
        "status_code":status.HTTP_200_OK,
        "meassage":"Info about female students only",
        "count":count,
        "data":rows
    }
    



