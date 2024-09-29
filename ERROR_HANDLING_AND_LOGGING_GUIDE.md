# Error Handling and Logging Guide

This guide provides instructions on how to implement error handling and logging in the microservices of our Face Recognition Attendance System. Follow these steps for each service (authentication, attendance, notification, and analytics).

## 1. Import necessary modules

Add the following imports at the top of your service's main file (e.g., `app.py`):

```python
import logging
from logging.handlers import RotatingFileHandler
import os
```

## 2. Set up logging

Add the following code near the top of your file, after the imports:

```python
# Setup logging
logger = logging.getLogger("service_name_service")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("service_name_service.log", maxBytes=10000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
```

Replace `"service_name"` with the name of your service (e.g., "authentication", "attendance", etc.).

## 3. Wrap database and external service connections in try-except blocks

For any database or external service connections (e.g., Redis, RabbitMQ), wrap the connection code in a try-except block:

```python
try:
    # Connection code here
    logger.info("Connection established successfully")
except Exception as e:
    logger.error(f"Error establishing connection: {str(e)}")
    raise
```

## 4. Add error handling to route handlers

For each route handler, add try-except blocks to catch and log errors:

```python
@app.post("/example-route")
async def example_route(data: SomeModel):
    try:
        # Route logic here
        logger.info("Operation completed successfully")
        return {"message": "Success"}
    except SomeSpecificException as e:
        logger.error(f"Specific error occurred: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Specific error message")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
```

## 5. Log important events

Throughout your code, add log messages for important events:

```python
logger.info("User logged in: {user_id}")
logger.warning("Failed login attempt for user: {username}")
logger.error("Database query failed: {query}")
```

## 6. Use environment variables for service URLs

Replace hardcoded service URLs with environment variables:

```python
service_url = os.getenv("SERVICE_URL", "http://default-service-url:8000")
```

## 7. Handle external service calls

When making calls to other services, use try-except blocks and log any errors:

```python
async with httpx.AsyncClient() as client:
    try:
        response = await client.post(f"{service_url}/endpoint", json=data)
        response.raise_for_status()
        logger.info("Successfully called external service")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred while calling external service: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error calling external service")
    except Exception as e:
        logger.error(f"Unexpected error calling external service: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
```

## 8. Update requirements.txt

Ensure that your `requirements.txt` file includes the necessary packages for logging and error handling. Add or update the following lines:

```
fastapi==0.68.0
uvicorn==0.15.0
httpx==0.23.0
```

## 9. Update Dockerfile

Make sure your Dockerfile copies the log file to the container and sets up a volume for persistent logging:

```dockerfile
# ... (other Dockerfile contents)

# Copy the log file
COPY service_name_service.log .

# Set up a volume for logs
VOLUME /app/logs

# ... (rest of Dockerfile)
```

Replace `service_name` with the name of your service.

## 10. Update docker-compose.yml

Add a volume for each service's logs in the `docker-compose.yml` file:

```yaml
services:
  service_name:
    # ... (other service configuration)
    volumes:
      - ./logs/service_name:/app/logs

# ... (at the end of the file)
volumes:
  service_name_logs:
```

Replace `service_name` with the name of your service.

By following these steps for each service, you'll ensure consistent error handling and logging across your microservices architecture. This will greatly improve the debuggability and maintainability of your system.