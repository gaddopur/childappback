import cv2
import numpy as np
from collections import deque
from mediapipe.python.solutions.face_mesh import FaceMesh

# Calibration settings
calibration_mode = True
calibration_data = {
    'ear': [],
    'mar': [],
    'brow_ratio': []
}

# Configuration Constants
FACE_MESH_CONFIG = {
    'min_detection_confidence': 0.7,
    'min_tracking_confidence': 0.7,
    'max_num_faces': 1,
    'refine_landmarks': True
}

THRESHOLDS = {
    'EAR_BLINK': 0.21,      # Eye Aspect Ratio for blink detection
    'EAR_SURPRISE': 0.30,   # Eye open threshold for surprise
    'MAR_SMILE': 0.30,      # Mouth Aspect Ratio for smile
    'MAR_SAD': 0.18,        # Mouth Aspect Ratio for sad
    'BROW_RAISE': 0.45,     # Brow raise threshold
    'BROW_FURROW': 0.3      # Brow furrow threshold
}

# Temporal smoothing and blink cooldown
EMOTION_HISTORY = deque(maxlen=5)  # 5-frame window
BLINK_COOLDOWN = 10                # Frames between allowed blinks
frame_counter = 0
last_blink_frame = 0

# Landmark Indices
LANDMARK_INDICES = {
    'MOUTH_LEFT': 61,
    'MOUTH_RIGHT': 291,
    'MOUTH_TOP': 0,
    'MOUTH_BOTTOM': 17,
    'LEFT_EYE_TOP': 159,
    'LEFT_EYE_BOTTOM': 145,
    'RIGHT_EYE_TOP': 386,
    'RIGHT_EYE_BOTTOM': 374,
    'LEFT_EYEBROW_INNER': 70,
    'RIGHT_EYEBROW_INNER': 300,
    'NOSE_TIP': 4
}

# Initialize Face Mesh
face_mesh = FaceMesh(**FACE_MESH_CONFIG)

def calibrate_frame(features):
    """Collect calibration data."""
    calibration_data['ear'].append((features['left_ear'] + features['right_ear']) / 2)
    calibration_data['mar'].append(features['mouth_ratio'])
    calibration_data['brow_ratio'].append(features['brow_ratio'])

def calculate_thresholds():
    """Compute and display suggested thresholds based on calibration data."""
    avg_ear = np.mean(calibration_data['ear'])
    std_ear = np.std(calibration_data['ear'])
    avg_mar = np.mean(calibration_data['mar'])
    std_mar = np.std(calibration_data['mar'])
    avg_brow = np.mean(calibration_data['brow_ratio'])
    std_brow = np.std(calibration_data['brow_ratio'])

    print("\nCalibration Complete!")
    print(f"Suggested EAR_BLINK threshold: {avg_ear - std_ear * 1.5:.2f}")
    print(f"Suggested EAR_SURPRISE threshold: {avg_ear + std_ear * 1.5:.2f}")
    print(f"Suggested MAR_SMILE threshold: {avg_mar + std_mar * 1.5:.2f}")
    print(f"Suggested MAR_SAD threshold: {avg_mar - std_mar * 1.5:.2f}")
    print(f"Suggested BROW_RAISE threshold: {avg_brow + std_brow * 1.5:.2f}")
    print(f"Suggested BROW_FURROW threshold: {avg_brow - std_brow * 1.5:.2f}")

def get_facial_features(landmarks, frame_shape):
    h, w = frame_shape[:2]
    features = {}
    
    # Convert landmarks to pixel coordinates
    coords = {name: (landmarks.landmark[idx].x * w,
              landmarks.landmark[idx].y * h)
              for name, idx in LANDMARK_INDICES.items()}
    
    # Mouth Analysis
    mouth_width = np.linalg.norm(np.array(coords['MOUTH_LEFT']) - np.array(coords['MOUTH_RIGHT']))
    mouth_height = np.linalg.norm(np.array(coords['MOUTH_TOP']) - np.array(coords['MOUTH_BOTTOM']))
    features['mouth_ratio'] = mouth_height / mouth_width if mouth_width != 0 else 0
    
    # Eye Analysis
    left_eye_vert = np.linalg.norm(np.array(coords['LEFT_EYE_TOP']) - coords['LEFT_EYE_BOTTOM'])
    right_eye_vert = np.linalg.norm(np.array(coords['RIGHT_EYE_TOP']) - coords['RIGHT_EYE_BOTTOM'])
    eye_horiz_ref = np.linalg.norm(np.array(coords['MOUTH_LEFT']) - coords['MOUTH_RIGHT'])
    
    features['left_ear'] = left_eye_vert / eye_horiz_ref if eye_horiz_ref != 0 else 0
    features['right_ear'] = right_eye_vert / eye_horiz_ref if eye_horiz_ref != 0 else 0
    
    # Eyebrow Analysis
    left_brow_dist = np.linalg.norm(np.array(coords['LEFT_EYEBROW_INNER']) - coords['NOSE_TIP'])
    right_brow_dist = np.linalg.norm(np.array(coords['RIGHT_EYEBROW_INNER']) - coords['NOSE_TIP'])
    features['brow_ratio'] = (left_brow_dist + right_brow_dist) / (2 * eye_horiz_ref)
    
    return features

def draw_landmarks(frame, landmarks, frame_shape):
    """Draw circles on the key landmarks used for emotion detection."""
    h, w = frame_shape[:2]
    for name, idx in LANDMARK_INDICES.items():
        x, y = int(landmarks.landmark[idx].x * w), int(landmarks.landmark[idx].y * h)
        color = (0, 255, 0)  # Green for visibility
        cv2.circle(frame, (x, y), 3, color, -1)
        cv2.putText(frame, name, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1)

def detect_emotion(features):
    global last_blink_frame, frame_counter
    
    emotion_scores = {
        'happy': 0,
        'sad': 0,
        'surprised': 0,
        'angry': 0,
        'neutral': 0,
        'blinking': 0
    }
    
    # Calculate eye metrics
    avg_ear = (features['left_ear'] + features['right_ear']) / 2
    
    # Cross-feature validation
    # Surprise requires both high EAR and brow raise
    if avg_ear > THRESHOLDS['EAR_SURPRISE'] and features['brow_ratio'] > THRESHOLDS['BROW_RAISE']:
        emotion_scores['surprised'] += 2.0
        
    # Angry requires low MAR + brow furrow
    if features['mouth_ratio'] < THRESHOLDS['MAR_SAD'] and features['brow_ratio'] < THRESHOLDS['BROW_FURROW']:
        emotion_scores['angry'] += 2.0
        
    # Happy requires high MAR without brow furrow
    if features['mouth_ratio'] > THRESHOLDS['MAR_SMILE'] and features['brow_ratio'] > THRESHOLDS['BROW_FURROW']:
        emotion_scores['happy'] += 2.0
    
    # Blink detection with cooldown and both-eye check
    if (frame_counter - last_blink_frame > BLINK_COOLDOWN and
        features['left_ear'] < THRESHOLDS['EAR_BLINK'] and
        features['right_ear'] < THRESHOLDS['EAR_BLINK']):
        emotion_scores['blinking'] += 2.0
        last_blink_frame = frame_counter
    
    # Temporal smoothing
    EMOTION_HISTORY.append(max(emotion_scores, key=emotion_scores.get))
    final_emotion = max(set(EMOTION_HISTORY), key=lambda x: EMOTION_HISTORY.count(x))
    
    return final_emotion

# Camera initialization with calibration instructions
print("Calibration Guide:")
print("1. Maintain neutral face position")
print("2. Note the displayed EAR/MAR values")
print("3. Adjust thresholds in THRESHOLDS dictionary accordingly\n")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    for i in [1, 2, 3]:
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            break

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

# Color coding for emotions
EMOTION_COLORS = {
    'happy': (0, 255, 0),
    'sad': (255, 0, 0),
    'surprised': (0, 165, 255),
    'angry': (0, 0, 255),
    'neutral': (255, 255, 255),
    'blinking': (255, 255, 0)
}

# Main loop
while True:
    success, frame = cap.read()
    if not success:
        break

    frame_counter += 1
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)
    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        features = get_facial_features(face_landmarks, frame.shape)

        if calibration_mode:
            calibrate_frame(features)
            cv2.putText(frame, "Calibrating... Maintain Neutral Face", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            if frame_counter > 100:  # Collect calibration data for 100 frames
                calibration_mode = False
                calculate_thresholds()
        else:
            emotion = detect_emotion(features)
            avg_ear = (features['left_ear'] + features['right_ear']) / 2
            mar = features['mouth_ratio']
            brow = features['brow_ratio']

            color = EMOTION_COLORS.get(emotion, (255, 255, 255))
            cv2.putText(frame, f"Emotion: {emotion}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            cv2.putText(frame, f"MAR: {mar:.2f}", (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            cv2.putText(frame, f"Brow: {brow:.2f}", (20, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        # Draw landmarks for emotion detection
        draw_landmarks(frame, face_landmarks, frame.shape)

    cv2.imshow('Enhanced Emotion Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()