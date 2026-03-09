from itertools import count
from typing_extensions import Annotated
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException,status
from load_data import load_data
import sqlite3
from pydantic import BaseModel, Field



load_data()
app = FastAPI()    

@app.get("/")

def redirect():
    return RedirectResponse(url="/details")


@app.get("/details")

def sort_details(sort_by:str | None=None):
    print(sort_by)
    if(sort_by):
        if(sort_by.lower() in ("age","medu","fedu","studytime","traveltime","freetime")):
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM students ORDER BY {sort_by} DESC")
            result = cursor.fetchall()
            conn.close()
            return {
                "status":"success",
                "status_code":status.HTTP_200_OK,
                "message":f"data sorted by {sort_by}",
                "data": result
            }
        
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "status":"error",
                    "message":"Invalid parameter for sorting, only age, medu, fedu, studytime, traveltime and freetime are allowed"
                }
            )
        
    else:
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
    


@app.get("/students/{gender}")

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


'''
school	sex	age	address	famsize	Pstatus	Medu	Fedu	 defualt - Mjob	 Fjob reason	guardian

n/a values

traveltime	studytime	failures	schoolsup	famsup	paid	activities	nursery	higher	
internet	romantic	famrel	freetime	goout	Dalc	Walc	health	absences	G1	G2	G3
'''

class pydantic_model(BaseModel):
    school: Annotated[str, Field(...,max_length=50, description="school name to which student belongs to")]
    sex: Annotated[str, Field(...,max_length=1, description="gender of student, only M and F are allowed")]
    age: Annotated[int, Field(..., ge=0, description="age of student")]
    address:Annotated[str,Field(...,max_length=150,description="address of student")]
    famsize:Annotated[str,Field(...,max_length=10,description="family size of student, only LE3 and GT3 are allowed")]
    Pstatus:Annotated[str,Field(default="A",max_length=1,description="parent's cohabitation status, only T and A are allowed")]
    Medu:Annotated[int,Field(default=4,ge=0,le=4,description="mother's education level, only 0 to 4 are allowed")]
    Fedu:Annotated[int,Field(default=4,ge=0,le=4,description="father's education level, only 0 to 4 are allowed")]
    Mjob:Annotated[str,Field(default="other",max_length=50,description="mother's    job, only teacher, health, services, at_home and other are allowed")]
    Fjob:Annotated[str,Field(default="other",max_length=50,description="father's job, only teacher, health, services, at_home and other are allowed")]

    reason:Annotated[str,Field(default="N/A",description="reason for choosing the school, only course preference, home proximity, reputation and other are allowed")]
    guardian:Annotated[str,Field(default="N/A",description="student's guardian, only mother, father and other are allowed")] 
    traveltime:Annotated[int,Field(default=0,description="home to school travel time, only 1 to 4 are allowed")]
    studytime:Annotated[int,Field(default=0,description="weekly study time, only 1 to 4 are allowed")]
    failures:Annotated[int,Field(default=0,description="number of past class failures, only 0 to 3 are allowed")]
    schoolsup:Annotated[str,Field(default="N/A",description="extra educational support, only yes and no are allowed")]
    famsup:Annotated[str,Field(default="N/A",description="family educational support, only yes and no are allowed")]
    paid:Annotated[str,Field(default="N/A",description="extra paid classes within the course subject, only yes and no are allowed")]
    activities:Annotated[str,Field(default="N/A",description="extra curricular activities, only yes and no are allowed")]
    nursery:Annotated[str,Field(default="N/A",description="attendance to nursery school, only yes and no are allowed")]
    higher:Annotated[str,Field(default="N/A",description="wants to take higher education, only yes and no are allowed")]
    internet:Annotated[str,Field(default="N/A",description="internet access at home, only yes and no are allowed")]
    romantic:Annotated[str,Field(default="N/A",max_length=3,description="with a romantic relationship, only yes and no are allowed")]
    famrel:Annotated[int,Field(default=0,description="quality of family relationships, only 1 to 5 are allowed")]
    freetime:Annotated[int,Field(default=0,description="free time after school, only 1 to 5 are allowed")]
    goout:Annotated[int,Field(default=0,description="going out with friends, only 1 to 5 are allowed")]
    Dalc:Annotated[int,Field(default=0,description="workday alcohol consumption, only 1 to 5 are allowed")]
    Walc:Annotated[int,Field(default=0,description="weekend alcohol consumption, only 1 to 5 are allowed")]
    health:Annotated[int,Field(default=0,description="current health status, only 1 to 5 are allowed")]
    absences:Annotated[int,Field(default=0,description="number of school absences")]
    G1:Annotated[int,Field(default=0,description="first period grade, only 0 to 20 are allowed")]
    G2:Annotated[int,Field(default=0,description="second period grade, only 0 to 20 are allowed")]
    G3:Annotated[int,Field(default=0,description="final grade, only 0 to 20 are allowed")]  


@app.post("/add_student")

def add_student(student: pydantic_model):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    prev_count = cursor.fetchone()[0]
    cursor.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (student.school, student.sex, student.age, student.address, student.famsize, student.Pstatus, student.Medu, 
                    student.Fedu, student.Mjob, student.Fjob, student.reason, student.guardian, student.traveltime, 
                    student.studytime, student.failures, student.schoolsup, student.famsup, student.paid, student.activities, 
                    student.nursery, student.higher, student.internet, student.romantic, student.famrel, student.freetime, 
                    student.goout, student.Dalc, student.Walc, student.health, student.absences, student.G1, student.G2, student.G3))
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM students")
    after_count = cursor.fetchone()[0]
    conn.close()
    return {
        "status":"success",
        "status_code":status.HTTP_200_OK,
        "message":f"student added successfully , previous count was {prev_count} and after count was {after_count}",
    }


@app.delete("/delete_student")

def delete_student(age:int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(age) FROM students")
    max_age = cursor.fetchone()[0]

    prev_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    count_agegrp = conn.execute("SELECT COUNT(*) FROM students WHERE age = ?",(age,)).fetchone()[0]

    if(age < max_age and age >= 0):
        cursor.execute("DELETE FROM students WHERE age=?",(age,))
        print(age)
        conn.commit()
        after_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        print(after_count)
        conn.close()
        return {
            "status":"success",
            "status_code":status.HTTP_200_OK,
            "message":f"students with age {age} group deleted successfully and before count {prev_count} and after count {after_count} and no of students with that age group was {count_agegrp} "
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"age should be >0 and <{max_age}"
        )
