import math

# Índices de landmarks que forman cada ojo (modelo de 468 puntos)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]

def _dist(p1, p2):
    """Devuelve la distancia euclídea entre dos puntos (x, y)."""
    return math.dist(p1, p2)

def _landmark_to_pixel(landmark, img_w, img_h):
    """
    Convierte un landmark normalizado (propiedades .x y .y en [0,1])
    a coordenadas en píxeles según el tamaño de la imagen.
    Devuelve (x:int, y:int).
    """
    return int(landmark.x * img_w), int(landmark.y * img_h)

def eye_aspect_ratio(landmarks, eye_indexes, img_shape):
    """
    Calcula el Eye Aspect Ratio (EAR) para un ojo.
    - landmarks: secuencia de landmarks (cada uno con .x y .y).
    - eye_indexes: lista de 6 índices que definen los puntos del ojo.
    - img_shape: forma de la imagen (h, w, channels).
    Pasos:
      1) Convertir los 6 landmarks del ojo a coordenadas de píxel.
      2) Calcular dos distancias verticales (v1, v2) y la distancia horizontal (hdist).
      3) Aplicar la fórmula EAR = (v1 + v2) / (2 * hdist).
    Retorna el EAR como float.
    """
    h, w, _ = img_shape  # alto y ancho de la imagen
    pts = []
    for idx in eye_indexes:
        lm = landmarks[idx]                   # obtener landmark por índice
        x, y = _landmark_to_pixel(lm, w, h)   # convertir a píxel
        pts.append((x, y))

    # Desempaquetar los 6 puntos para claridad semántica
    p0, p1, p2, p3, p4, p5 = pts

    # Dos medidas verticales (pares superior-inferior)
    v1 = _dist(p1, p4)
    v2 = _dist(p2, p5)

    # Medida horizontal (esquinas del ojo)
    hdist = _dist(p0, p3)

    # Cálculo final del EAR
    ear = (v1 + v2) / (2.0 * hdist)
    return ear

def compute_average_ear(landmarks, img_shape):
    """
    Calcula el EAR promedio de ambos ojos.
    Retorna una tupla: (ear_promedio, ear_izquierdo, ear_derecho).
    """
    ear_left = eye_aspect_ratio(landmarks, LEFT_EYE, img_shape)
    ear_right = eye_aspect_ratio(landmarks, RIGHT_EYE, img_shape)
    ear = (ear_left + ear_right) / 2.0
    return ear, ear_left, ear_right