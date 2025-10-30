from metrics.eye_metrics import compute_average_ear
from metrics.mouth_metrics import mouth_aspect_ratio

class DrowinessAnalyzer:
    """
        Mantiene estado entre frames (contadores/temporizadores) y decide:
        - eyes_closed: ojo cerrado por EAR
        - yawn: bostezo por MAR
        - drowsy: somnolencia si ojos cerrados N frames
    """
    def __init__(self,
                 ear_threshold = 0.23,
                 frames_threshold = 15,
                 mar_threshold = 0.5,
                 yawn_frames_threshold = 12):
        self.ear_threshold = ear_threshold
        self.frames_threshold = frames_threshold
        self.mar_threshold = mar_threshold
        self.yawn_frames_threshold = yawn_frames_threshold

        self.closed_frames = 0
        self.yawn_frames = 0
        self.cooldown = 0
        self.cooldown_time = 30

    def analyze(self, landmarks, img_shape):
        ear, ear_l, ear_r = compute_average_ear(landmarks, img_shape)
        mar = mouth_aspect_ratio(landmarks, img_shape)

        # ojos
        if ear < self.ear_threshold:
            self.closed_frames += 1 # contador de frames de ojo cerrado
        else:
            self.closed_frames = 0 # reset si ojo abierto

        eyes_closed = self.closed_frames > 0
        drowsy = self.closed_frames >= self.frames_threshold

        # bostezo
        if mar > self.mar_threshold:
            self.yawn_frames += 1 # contador de frames de bostezo
        else:
            self.yawn_frames = 0 # reset si no hay bostezo

        yawn = self.yawn_frames > self.yawn_frames_threshold

        if self.cooldown > 0:
            self.cooldown -= 1

        return{
            "ear": ear,
            "ear_left": ear_l,
            "ear_right": ear_r,
            "mar": mar,
            "eyes_closed": eyes_closed,
            "yawn": yawn,
            "drowsy": drowsy,
            "should_beep": drowsy and self.cooldown == 0
        }

    def mark_alert_played(self):
        # Llamar tras reproducir alerta para iniciar cooldown
        self.cooldown = self.cooldown_time


