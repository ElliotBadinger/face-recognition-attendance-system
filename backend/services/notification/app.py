from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI()

# This is a mock database. In a real application, you'd use a proper database.
notifications_db = {}

class Notification(BaseModel):
    id: str
    user_id: str
    message: str
    timestamp: datetime
    read: bool

class NotificationCreate(BaseModel):
    user_id: str
    message: str

@app.post("/notifications/", response_model=Notification)
async def create_notification(notification: NotificationCreate):
    notification_id = str(uuid.uuid4())
    new_notification = Notification(
        id=notification_id,
        user_id=notification.user_id,
        message=notification.message,
        timestamp=datetime.now(),
        read=False
    )
    notifications_db[notification_id] = new_notification
    return new_notification

@app.get("/notifications/{notification_id}", response_model=Notification)
async def read_notification(notification_id: str):
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notifications_db[notification_id]

@app.get("/notifications/user/{user_id}")
async def read_user_notifications(user_id: str):
    user_notifications = [notif for notif in notifications_db.values() if notif.user_id == user_id]
    return user_notifications

@app.put("/notifications/{notification_id}/read")
async def mark_notification_as_read(notification_id: str):
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Notification not found")
    notifications_db[notification_id].read = True
    return {"message": "Notification marked as read"}

@app.delete("/notifications/{notification_id}")
async def delete_notification(notification_id: str):
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Notification not found")
    del notifications_db[notification_id]
    return {"message": "Notification deleted successfully"}