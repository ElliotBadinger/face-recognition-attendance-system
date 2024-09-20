FROM python:3.9

WORKDIR /app

# Install system dependencies for face_recognition
RUN apt-get update && apt-get install -y \
    cmake \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]