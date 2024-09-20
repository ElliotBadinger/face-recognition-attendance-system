# Face Recognition Attendance System

This project is a microservices-based face recognition attendance system. It consists of several services that work together to provide face recognition, user management, authentication, attendance tracking, notifications, and analytics.

## Project Structure

```
.
├── frontend
│   ├── index.html
│   └── main.py
├── backend
│   ├── services
│   │   ├── face_recognition
│   │   ├── user_management
│   │   ├── authentication
│   │   ├── attendance
│   │   ├── notification
│   │   └── analytics
│   └── api_gateway
├── docker-compose.yml
└── README.md
```

## Prerequisites

- Docker
- Docker Compose

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd face-recognition-attendance-system
   ```

2. Create a `.env` file in the root directory and add the following environment variables:
   ```
   SECRET_KEY=your_secret_key_here
   ```

3. Build and start the services:
   ```
   docker-compose up --build
   ```

4. The services will be available at the following ports:
   - API Gateway: http://localhost:3000
   - Face Recognition Service: http://localhost:8000
   - User Management Service: http://localhost:8001
   - Authentication Service: http://localhost:8002
   - Attendance Service: http://localhost:8003
   - Notification Service: http://localhost:8004
   - Analytics Service: http://localhost:8005

## Usage

1. Open the frontend application by opening `frontend/index.html` in a web browser.

2. Use the UI to interact with the various services:
   - Register new users
   - Authenticate users
   - Upload images for face recognition
   - View attendance records
   - Check notifications
   - View analytics

## API Documentation

For detailed API documentation, refer to the `api_contracts.md` file in the root directory.

## Development

To make changes to the services:

1. Modify the code in the respective service directories.
2. Rebuild and restart the services:
   ```
   docker-compose up --build
   ```

## Testing

To test the face recognition:

1. Ensure you have added known face images to the `frontend/known_faces` directory.
2. Use the frontend to upload an image for recognition.

To test other services, use the frontend UI or send requests directly to the API endpoints as described in the API documentation.

## Troubleshooting

If you encounter any issues:

1. Ensure all containers are running:
   ```
   docker-compose ps
   ```
2. Check container logs:
   ```
   docker-compose logs <service_name>
   ```
3. Restart the services:
   ```
   docker-compose down
   docker-compose up --build
   ```

## Security Considerations

- This is a basic setup and may need additional security measures for production use.
- Ensure to use strong, unique passwords and keep the SECRET_KEY secure.
- Implement proper input validation and sanitization in all services.
- Use HTTPS for all communications in a production environment.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.