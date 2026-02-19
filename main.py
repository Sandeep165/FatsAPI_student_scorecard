'''
1) Student Score Tracker

A small API to store student records and compute grade averages.
'''
from fastapi import FastAPI, HTTPException, Path
import fastapi
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import List, Optional, Dict, Annotated, Literal

class Student(BaseModel):
    id : Annotated[str, Field(..., description="ID of the student", examples=["S001"])]
    name : Annotated[str, Field(..., description="Name of the student", examples=["Alice Smith"])]
    scores : Annotated[List[int], Field(..., description="List of scores for the student", examples=[[85.5, 90.0, 78.0]])]

    @computed_field
    @property
    def user_name(self) -> str:
        return self.name + self.id
    
    @computed_field
    @property
    def max_score(self) -> int:
        return max(self.scores)
    
    @computed_field
    @property
    def avg_score(self) -> int:
        return int(sum(self.scores)/len(self.scores))
    
    @computed_field
    @property
    def grade(self) -> str:
        if self.avg_score >= 90:
            return "A"
        elif self.avg_score >= 80:
            return "B"      
        elif self.avg_score >= 70:
            return "C"  
        elif self.avg_score >= 60:
            return "D"


class Update_student(BaseModel):
    id :Annotated[Optional[str], Field(default=None, description="ID of the student", examples=["S001"])]
    name : Annotated[Optional[str], Field(default=None, description="Name of the student", examples=["Alice Smith"])]
    scores : Annotated[Optional[List[int]], Field(default=None, description="List of scores for the student", examples=[[85.5, 90.0, 78.0]])]   
    
'''
GET /student  → list of all students

GET /student/{id} → return single record

POST /student → add new record

PUT /student/{id} → update record

DELETE /student/{id} → delete record

'''           

app = FastAPI()

def load_data():
    with open("students.json" , "r") as f:
        data = json.load(f)
    return data
        
    
def save_data(data):
    with open("students.json", "w") as f:
        json.dump(data, f)

@app.get("/students")
def view():
    data = load_data()
    return data

@app.get("/student/{id}")
def view_student(id : str = Path(description="View students based on ID")):
    student_data = load_data()
    
    if id not in student_data:
        raise HTTPException(status_code=404, detail="Student not found in the data")
    return student_data[id]

@app.get("/student/{id}/subjects")
def view_student(id : str):
    student_data = load_data()
    
    if id not in student_data:
        raise HTTPException(status_code=404, detail="Student not found in the data")
    subject_val = student_data[id].get("subjects")
    
    if subject_val is None:
        raise HTTPException(status_code=404, detail="Subject not found for the student")
    return subject_val
    
    
@app.post("/create_student")
def create_student(student : Student):
    student_data = load_data()
    
    if student.id in student_data:
        raise HTTPException(status_code=401 , detail="Student is already present in the data")
    
    student_data[student.id] = student.model_dump(exclude=["id"])
    
    #save the data back to the file
    save_data(student_data)
    return JSONResponse(status_code=200, content="Student data added successfully")
    
@app.put("/update_student/{id}")
def update_student_data(id, student : Update_student):
    student_data = load_data()
    
    if id not in student_data:
        raise HTTPException(status_code=404, detail="Given student is not there in the data")
    
    existing_data = student_data[id]
    current_data = student.model_dump(exclude_unset=True)
    
    for k,v in current_data.items():
        existing_data[k] = v
        
    existing_data["id"] = student.id
    student_pydantic_obj = Student(**existing_data)
    
    existing_data = student_pydantic_obj.model_dump(exclude="id")
    
    student_data[id] = existing_data
    
    
    save_data(student_data)
    return JSONResponse(status_code=200, content="Student data updated successfully !!")
    
    
@app.delete("/student/{id}")
def delete_student(id : str):
    student_data = load_data()
    
    if id not in student_data:
        raise HTTPException(status_code=404, detail="Student not found !!")
    
    del student_data[id]
    
    save_data(student_data)
    
    return JSONResponse(status_code=200, content=f"Student data for id :- {id} has been deleted")