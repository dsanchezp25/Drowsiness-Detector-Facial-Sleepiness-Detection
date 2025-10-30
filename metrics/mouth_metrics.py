import math

# Landmarks de Mediapipe para la boca:
# Vertical: labio superior (13), labio inferior (14)
# Horizontal: comisuras de los labios izquierda (78) y derecha (308)
UPPER_LIP = 13
LOWER_LIP = 14
LEFT_MOUTH = 78
RIGHT_MOUTH = 308

def _dist(p1, p2):
    return math.dist(p1, p2)

def _lm_to_px(landmark, frame_width, frame_height):
    return int(landmark.x * frame_width), int(landmark.y * frame_height)

def mouth_aspect_ratio(landmarks, img_shape):
    h, w, _ = img_shape

    ul = _lm_to_px(landmarks[UPPER_LIP], w, h) # labio superior
    ll = _lm_to_px(landmarks[LOWER_LIP], w, h) # labio inferior
    ml = _lm_to_px(landmarks[LEFT_MOUTH], w, h) # comisura izquierda
    mr = _lm_to_px(landmarks[RIGHT_MOUTH], w, h) # comisura derecha

    vertical = _dist(ul, ml)
    horizontal = _dist(ml, mr)

    if horizontal == 0:
        return 0.0 # evitar división por cero

    return vertical/horizontal