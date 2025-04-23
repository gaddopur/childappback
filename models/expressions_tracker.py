import cv2
from deepface import DeepFace
import numpy as np
from collections import deque

# Configure camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Windows-specific backend
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Emotion color coding
EMOTION_COLORS = {
    'happy': (0, 255, 0),     # Green
    'sad': (255, 0, 0),       # Blue
    'surprise': (0, 165, 255),# Orange
    'angry': (0, 0, 255),     # Red
    'fear': (255, 0, 127),    # Pink
    'disgust': (0, 255, 127), # Teal
    'neutral': (255, 255, 255)# White
}

# Temporal smoothing buffer
emotion_history = deque(maxlen=5)
frame_counter = 0

results = []

def analyze_frame(frame):
    try:
        return DeepFace.analyze(
            img_path=frame,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='opencv',
            silent=True
        )
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        return None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_counter += 1
    
    # Process every 5th frame
    if frame_counter % 5 == 0:
        results = analyze_frame(frame)
    
    if results:
        try:
            face = results[0]
            emotion = face['dominant_emotion']
            emotion_history.append(emotion)
            
            final_emotion = max(set(emotion_history), 
                              key=lambda x: emotion_history.count(x))
            
            x = face['region']['x']
            y = face['region']['y']
            w = face['region']['w']
            h = face['region']['h']
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), EMOTION_COLORS[final_emotion], 2)
            cv2.putText(frame, f"{final_emotion}", 
                       (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 
                       EMOTION_COLORS[final_emotion], 2)
            
        except KeyError:
            pass
    
    cv2.imshow('Emotion Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()