import logging
import face_recognition
import cv2
import time
import datetime
import os
from flask import Flask, jsonify, request, send_from_directory, Response
import threading
import numpy as np
import socket

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.')

# Initialize known face encodings and names
known_face_encodings = []
known_face_names = []

# Initialize attendance status
attendance = {}

# Get current date and time
date = datetime.datetime.now()
current_date = date.strftime("DATE: %d %b")
current_time = date.strftime("%H:%M")

period = f"PERIOD: 1  {current_date}"

# Create a lock for thread-safe operations
lock = threading.Lock()

# Global variable for the camera
camera = None

def load_known_faces():
    global known_face_encodings, known_face_names
    known_face_encodings = []
    known_face_names = []
    try:
        # Create the 'known_faces' directory if it doesn't exist
        os.makedirs('known_faces', exist_ok=True)
        
        face_files = [f for f in os.listdir('known_faces') if f.endswith(('.jpg', '.png'))]
        
        if not face_files:
            logger.warning("No known faces found in the 'known_faces' directory")
            return

        for filename in face_files:
            name = os.path.splitext(filename)[0]
            image_path = os.path.join('known_faces', filename)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)
            
            if encoding:
                known_face_encodings.append(encoding[0])
                known_face_names.append(name)
            else:
                logger.warning(f"No face found in {filename}, skipping")

        logger.info(f"Loaded {len(known_face_names)} known faces")
    except Exception as e:
        logger.error(f"Error loading known faces: {str(e)}")

# Load initial known faces
load_known_faces()

def check_for_faces(frame):
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        return face_recognition.face_encodings(rgb_frame, face_locations), face_locations
    except Exception as e:
        logger.error(f"Error checking for faces: {str(e)}")
        return [], []

def process_frame(frame):
    face_encodings, face_locations = check_for_faces(frame)
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        with lock:
            attendance[name] = "present"
    
    return face_locations, [name for name in attendance if attendance[name] == "present"]

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/get_attendance', methods=['GET'])
def get_attendance():
    try:
        with lock:
            attendance_data = [
                {
                    "id": i + 1,
                    "name": name,
                    "status": status
                } for i, (name, status) in enumerate(attendance.items())
            ]
        return jsonify({
            "period": period,
            "current_time": datetime.datetime.now().strftime("%H:%M"),
            "attendance": attendance_data
        })
    except Exception as e:
        logger.error(f"Error getting attendance: {str(e)}")
        return jsonify({"message": "An error occurred while getting attendance"}), 500

@app.route('/api/reset_attendance', methods=['POST'])
def reset_attendance():
    try:
        global attendance
        with lock:
            attendance = {name: "absent" for name in known_face_names}
        logger.info("Attendance reset successfully")
        return jsonify({"message": "Attendance reset successfully"})
    except Exception as e:
        logger.error(f"Error resetting attendance: {str(e)}")
        return jsonify({"message": "An error occurred while resetting attendance"}), 500

@app.route('/api/add_learner', methods=['POST'])
def add_learner():
    try:
        if 'photo' not in request.files or 'name' not in request.form:
            return jsonify({"message": "Missing photo or name"}), 400

        photo = request.files['photo']
        name = request.form['name']

        if photo.filename == '':
            return jsonify({"message": "No selected file"}), 400

        if photo and name:
            # Create the 'known_faces' directory if it doesn't exist
            os.makedirs('known_faces', exist_ok=True)
            
            filename = f"{name}.jpg"
            photo.save(os.path.join('known_faces', filename))
            
            # Reload known faces
            load_known_faces()
            
            logger.info(f"Added new learner: {name}")
            return jsonify({"message": f"Learner {name} added successfully"})
    except Exception as e:
        logger.error(f"Error adding learner: {str(e)}")
        return jsonify({"message": "An error occurred while adding the learner"}), 500

@app.route('/process_frame', methods=['POST'])
def process_client_frame():
    if 'frame' not in request.files:
        return jsonify({"error": "No frame provided"}), 400
    
    frame_file = request.files['frame']
    frame_array = np.frombuffer(frame_file.read(), np.uint8)
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
    
    face_locations, recognized_names = process_frame(frame)
    
    return jsonify({
        "faces_detected": len(face_locations),
        "recognized_names": recognized_names,
        "attendance_updated": True
    })

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def gen_frames():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)  # 0 for default camera
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        ip_address = get_ip_address()
        logger.info(f"Server running on http://{ip_address}:5000")
        logger.info("Other users on the same network can access the application using this address.")
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    except Exception as e:
        logger.critical(f"Failed to start the server: {str(e)}")