# API Contracts

## Face Recognition Service

### POST /recognize
Request:
```
Content-Type: multipart/form-data

file: [image file]
```

Response:
```json
{
  "results": [
    {
      "name": "string",
      "confidence": 0.95
    }
  ]
}
```

## User Management Service

### GET /users/{user_id}
Response:
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

### POST /users
Request:
```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com"
}
```

Response:
```json
{
  "id": 124,
  "name": "Jane Doe",
  "email": "jane.doe@example.com"
}
```

## Authentication Service

### POST /token
Request:
```
Content-Type: application/x-www-form-urlencoded

username: string
password: string
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### GET /users/me
Headers:
```
Authorization: Bearer {access_token}
```

Response:
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe"
}
```

## Attendance Service

### POST /attendance
Request:
```json
{
  "user_id": "123",
  "location": "Office A"
}
```

Response:
```json
{
  "id": "456",
  "user_id": "123",
  "timestamp": "2023-05-20T09:00:00Z",
  "location": "Office A"
}
```

### GET /attendance/{attendance_id}
Response:
```json
{
  "id": "456",
  "user_id": "123",
  "timestamp": "2023-05-20T09:00:00Z",
  "location": "Office A"
}
```

### GET /attendance/user/{user_id}
Response:
```json
[
  {
    "id": "456",
    "user_id": "123",
    "timestamp": "2023-05-20T09:00:00Z",
    "location": "Office A"
  },
  {
    "id": "457",
    "user_id": "123",
    "timestamp": "2023-05-21T09:05:00Z",
    "location": "Office B"
  }
]
```

## Notification Service

### POST /notifications
Request:
```json
{
  "user_id": "123",
  "message": "Your attendance has been recorded."
}
```

Response:
```json
{
  "id": "789",
  "user_id": "123",
  "message": "Your attendance has been recorded.",
  "timestamp": "2023-05-20T09:01:00Z",
  "read": false
}
```

### GET /notifications/{notification_id}
Response:
```json
{
  "id": "789",
  "user_id": "123",
  "message": "Your attendance has been recorded.",
  "timestamp": "2023-05-20T09:01:00Z",
  "read": false
}
```

### GET /notifications/user/{user_id}
Response:
```json
[
  {
    "id": "789",
    "user_id": "123",
    "message": "Your attendance has been recorded.",
    "timestamp": "2023-05-20T09:01:00Z",
    "read": false
  },
  {
    "id": "790",
    "user_id": "123",
    "message": "Meeting reminder: Team sync at 2 PM.",
    "timestamp": "2023-05-20T13:00:00Z",
    "read": true
  }
]
```

## Analytics Service

### GET /analytics/attendance/summary
Response:
```json
{
  "total_records": 1000,
  "unique_users": 50,
  "locations": ["Office A", "Office B", "Home Office"]
}
```

### GET /analytics/attendance/user/{user_id}
Response:
```json
{
  "user_id": "123",
  "total_records": 20,
  "locations": ["Office A", "Home Office"],
  "first_record": "2023-05-01T09:00:00Z",
  "last_record": "2023-05-20T17:00:00Z"
}
```

### GET /analytics/attendance/daily
Query Parameters:
- start_date: YYYY-MM-DD
- end_date: YYYY-MM-DD

Response:
```json
{
  "2023-05-01": 45,
  "2023-05-02": 48,
  "2023-05-03": 50
}
```

### GET /analytics/attendance/location
Response:
```json
{
  "Office A": 500,
  "Office B": 300,
  "Home Office": 200
}
```

Note: All endpoints except for authentication require a valid JWT token in the Authorization header.