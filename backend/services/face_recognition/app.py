from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
import face_recognition
import numpy as np
import io
from PIL import Image
import os
import aio_pika
import json
import httpx
import logging
from logging.handlers import RotatingFileHandler

app = FastAPI()

# Setup logging
logger = logging.getLogger("face_recognition_service")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("face_recognition_service.log", maxBytes=10000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Load known faces
known_faces_dir = "known_faces"
known_face_encodings = []
known_face_names = []

try:
    for filename in os.listdir(known_faces_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(os.path.splitext(filename)[0])
    logger.info(f"Loaded {len(known_face_encodings)} known faces")
except Exception as e:
    logger.error(f"Error loading known faces: {str(e)}")

async def verify_token(token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{os.getenv('AUTHENTICATION_URL', 'http://authentication:8000')}/verify-token",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Token verification failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.error(f"Unexpected error during token verification: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@app.post("/recognize")
async def recognize_face(file: UploadFile = File(...), token: str = Depends(verify_token)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        np_image = np.array(image)

        face_locations = face_recognition.face_locations(np_image)
        face_encodings = face_recognition.face_encodings(np_image, face_locations)

        results = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            confidence = 0.0

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                confidence = 1 - face_distances[best_match_index]

            results.append({"name": name, "confidence": float(confidence)})

        # Send results to RabbitMQ
        await send_to_queue(results)

        # Record attendance
        await record_attendance(name, token)

        logger.info(f"Face recognition successful. Results: {results}")
        return JSONResponse(content={"results": results})
    except Exception as e:
        logger.error(f"Error during face recognition: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Face recognition failed")

async def send_to_queue(results):
    try:
        rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
        connection = await aio_pika.connect_robust(rabbitmq_url)
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue("face_recognition_results")

            message_body = json.dumps(results).encode()
            message = aio_pika.Message(body=message_body)

            await channel.default_exchange.publish(
                message, routing_key="face_recognition_results"
            )
        logger.info("Results sent to RabbitMQ successfully")
    except Exception as e:
        logger.error(f"Error sending results to RabbitMQ: {str(e)}")

async def record_attendance(name: str, token: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{os.getenv('ATTENDANCE_URL', 'http://attendance:8000')}/attendance/",
                json={"user_id": name, "location": "Office"},
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            logger.info(f"Attendance recorded for user: {name}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to record attendance: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error recording attendance: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)