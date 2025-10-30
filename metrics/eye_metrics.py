import math

from mediapipe.tasks.python.components.containers import landmark

# índices de los ojos en Mediapipe FaceMesh (468 puntos)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]

def _dist(p1, p2):
    return math.dist(p1, p2)

def _landmark_to_tuple(landmark, frame_width, frame_height):
    return int(landmark.x * frame_width), int(landmark.y * frame_height)

def eye_aspect_ratio(landmarks, eye_indices, img_shape):
    h, w, _ = img_shape
    pts = []
    for idx in eye_indices:
        lm = landmarks[idx]
        x, y = _landmark_to_tuple(lm, w, h)
        pts.append((x, y))

    p0, p1, p2, p3, p4, p5 = pts # puntos del ojo

    # vertices
    v1 = _dist(p1, p4)  # distancia vertical 1
    v2 = _dist(p2, p5)  # distancia vertical 2

    # horizontal
    h_dist = _dist(p0, p3)  # distancia horizontal

    ear = (v1 + v2) / (2.0 * h_dist) # fórmula del EAR
    return ear

def compute_average_ear(landmarks, img_shape):
    ear_left = eye_aspect_ratio(landmarks, LEFT_EYE, img_shape)
    ear_right = eye_aspect_ratio(landmarks, RIGHT_EYE, img_shape)
    ear = (ear_left + ear_right) / 2.0 # promedio de ambos ojos
    return ear, ear_left, ear_right
