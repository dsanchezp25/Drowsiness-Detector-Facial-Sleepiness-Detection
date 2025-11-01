import cv2
from alerts import sound_alert  # importa el módulo que reproduce alertas sonoras

def draw_status_banner(frame, text, top=10):
    """
    Dibuja una banda con texto en la parte superior izquierda del frame.
    - frame: imagen BGR (numpy array).
    - text: cadena a mostrar.
    - top: coordenada Y superior donde empezar a dibujar (ajustable).
    """
    h, w, _ = frame.shape  # alto y ancho del frame (no usado directamente pero útil si se amplía)
    pad = 6  # padding interior alrededor del texto
    # Obtener tamaño en píxeles del texto con la fuente y grosor deseados
    (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
    # Dibujar rectángulo negro como fondo de la banda (con padding)
    cv2.rectangle(
        frame,
        (8, top - 24),
        (8 + text_w + 2 * pad, top + text_h + 2 * pad),
        (0, 0, 0),
        -1
    )
    # Dibujar el texto en rojo encima del rectángulo
    cv2.putText(
        frame,
        text,
        (8 + pad, top + text_h),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

def draw_drowsy(frame):
    """
    Dibuja un aviso grande de somnolencia en el frame.
    Se usa para alertas visuales prominentes cuando se detecta somnolencia.
    """
    cv2.putText(
        frame,
        "DROWSINESS DETECTED",
        (50, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (0, 0, 255),
        3
    )

def draw_yawn(frame):
    """
    Dibuja un mensaje de aviso para bostezos/alertas y lanza la alerta sonora.
    - Llamar a esta función reproduce también el sonido mediante sound_alert.play_alert().
    """
    cv2.putText(
        frame,
        "ALERT! WAKE UP!",
        (50, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 0, 255),
        3
    )
    # Reproducir la alerta sonora (el módulo debe gestionar la reproducción y errores)
    sound_alert.play_alert()