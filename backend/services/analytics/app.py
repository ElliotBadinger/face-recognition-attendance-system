from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List

app = FastAPI()

# This is a mock database. In a real application, you'd use a proper database and perform actual analytics.
attendance_db = {}

class AttendanceRecord(BaseModel):
    id: str
    user_id: str
    timestamp: datetime
    location: str

class AttendanceSummary(BaseModel):
    total_records: int
    unique_users: int
    locations: List[str]

class UserAttendanceSummary(BaseModel):
    user_id: str
    total_records: int
    locations: List[str]
    first_record: datetime
    last_record: datetime

@app.get("/analytics/attendance/summary", response_model=AttendanceSummary)
async def get_attendance_summary():
    records = list(attendance_db.values())
    return AttendanceSummary(
        total_records=len(records),
        unique_users=len(set(record.user_id for record in records)),
        locations=list(set(record.location for record in records))
    )

@app.get("/analytics/attendance/user/{user_id}", response_model=UserAttendanceSummary)
async def get_user_attendance_summary(user_id: str):
    user_records = [record for record in attendance_db.values() if record.user_id == user_id]
    if not user_records:
        raise HTTPException(status_code=404, detail="No attendance records found for this user")
    
    return UserAttendanceSummary(
        user_id=user_id,
        total_records=len(user_records),
        locations=list(set(record.location for record in user_records)),
        first_record=min(record.timestamp for record in user_records),
        last_record=max(record.timestamp for record in user_records)
    )

@app.get("/analytics/attendance/daily")
async def get_daily_attendance(start_date: datetime, end_date: datetime):
    daily_counts = {}
    current_date = start_date
    while current_date <= end_date:
        daily_counts[current_date.date()] = 0
        current_date += timedelta(days=1)

    for record in attendance_db.values():
        if start_date <= record.timestamp <= end_date:
            daily_counts[record.timestamp.date()] += 1

    return daily_counts

@app.get("/analytics/attendance/location")
async def get_location_attendance():
    location_counts = {}
    for record in attendance_db.values():
        location_counts[record.location] = location_counts.get(record.location, 0) + 1
    return location_counts