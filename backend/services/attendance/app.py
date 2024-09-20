from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import List
import uuid

app = FastAPI()

# This is a mock database. In a real application, you'd use a proper database.
attendance_db = {}

class AttendanceRecord(BaseModel):
    id: str
    user_id: str
    timestamp: datetime
    location: str

class AttendanceCreate(BaseModel):
    user_id: str
    location: str

@app.post("/attendance/", response_model=AttendanceRecord)
async def create_attendance(attendance: AttendanceCreate):
    attendance_id = str(uuid.uuid4())
    new_attendance = AttendanceRecord(
        id=attendance_id,
        user_id=attendance.user_id,
        timestamp=datetime.now(),
        location=attendance.location
    )
    attendance_db[attendance_id] = new_attendance
    return new_attendance

@app.get("/attendance/{attendance_id}", response_model=AttendanceRecord)
async def read_attendance(attendance_id: str):
    if attendance_id not in attendance_db:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance_db[attendance_id]

@app.get("/attendance/user/{user_id}", response_model=List[AttendanceRecord])
async def read_user_attendance(user_id: str):
    user_attendance = [record for record in attendance_db.values() if record.user_id == user_id]
    return user_attendance

@app.put("/attendance/{attendance_id}", response_model=AttendanceRecord)
async def update_attendance(attendance_id: str, attendance: AttendanceCreate):
    if attendance_id not in attendance_db:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    updated_attendance = AttendanceRecord(
        id=attendance_id,
        user_id=attendance.user_id,
        timestamp=attendance_db[attendance_id].timestamp,
        location=attendance.location
    )
    attendance_db[attendance_id] = updated_attendance
    return updated_attendance

@app.delete("/attendance/{attendance_id}")
async def delete_attendance(attendance_id: str):
    if attendance_id not in attendance_db:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    del attendance_db[attendance_id]
    return {"message": "Attendance record deleted successfully"}