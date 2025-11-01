import time
from metrics.eye_metrics import compute_average_ear

class DrowsinessAnalyzer:
    """
    Analiza landmarks para detectar somnolencia usando EAR (Eye Aspect Ratio).
    - ear_threshold: umbral para considerar que el ojo está cerrado.
    - closed_seconds: segundos continuos que deben pasar con ojos cerrados para declarar somnolencia.
    - cooldown_seconds: tiempo mínimo tras una alarma antes de permitir otra.
    """

    def __init__(self, ear_threshold: float = 0.38, closed_seconds: float = 1.0):
        # Configuración
        self.ear_threshold = ear_threshold
        self.closed_seconds = closed_seconds

        # Estado dinámico
        self.is_closed = False         # si actualmente se considera que los ojos están cerrados
        self.closed_since = None       # timestamp (time.monotonic) de cuando se detectó el cierre
        self.in_drowsy_state = False   # si ya se ha declarado somnolencia (para UI/visual)
        self.cooldown = 0.0            # contador de cooldown restante en segundos
        self.cooldown_seconds = 1.0    # duración del cooldown tras reproducir alerta

    def analyze(self, landmarks, img_shape):
        """
        Analiza los landmarks y devuelve un diccionario con:
          - 'ear': EAR promedio
          - 'eyes_closed': booleano si los ojos están por debajo del umbral
          - 'drowsy': booleano si se considera somnoliento (cerrado >= closed_seconds)
          - 'should_beep': booleano si debe reproducirse la alarma ahora (toma en cuenta cooldown)
        Pasos:
          1. Calcular EAR de ambos ojos.
          2. Determinar si los ojos están cerrados comparando con ear_threshold.
          3. Si se acaban de cerrar, guardar el tiempo de inicio.
          4. Si llevan cerrados >= closed_seconds y no hay cooldown, marcar should_beep.
          5. Reducir el cooldown aprox. según FPS (se resta 1/30 s por llamada).
        """
        # 1) Calcular EAR promedio y por ojo
        ear, ear_l, ear_r = compute_average_ear(landmarks, img_shape)
        now = time.monotonic()  # tiempo monotónico para medir intervalos

        # 2) Comprobar si los ojos están cerrados según el umbral
        eyes_closed_now = ear < self.ear_threshold

        if eyes_closed_now:
            # Si antes no estaban cerrados, marcar inicio del cierre
            if not self.is_closed:
                self.is_closed = True
                self.closed_since = now
                print(f"[DEBUG] Ojos cerrados desde {self.closed_since}")
        else:
            # Si ahora están abiertos, resetar estado relacionado con cierre/somnolencia
            self.is_closed = False
            self.closed_since = None
            self.in_drowsy_state = False
            print(f"[DEBUG] Ojos abiertos, resetear estado.")

        should_beep = False

        # 3) Si están cerrados, comprobar duración
        if self.is_closed and self.closed_since is not None:
            elapsed = now - self.closed_since
            print(f"[DEBUG] Ojos cerrados por {elapsed:.2f} segundos.")
            if elapsed >= self.closed_seconds:
                # Si supera el umbral de tiempo y no estamos ya en estado somnoliento
                # y no hay cooldown, activar la alarma
                if not self.in_drowsy_state and self.cooldown <= 0:
                    should_beep = True
                    self.in_drowsy_state = True
                    # iniciar cooldown para evitar varias alarmas seguidas
                    self.cooldown = self.cooldown_seconds
                    print(f"[DEBUG] Drowsiness detected! Alarma activada.")

        # 4) Gestionar decremento del cooldown.
        # Aquí se resta un paso equivalente a ~1/30 s (suponer llamadas por frame ~30 FPS).
        if self.cooldown > 0:
            self.cooldown -= 1 / 30
            if self.cooldown < 0:
                self.cooldown = 0

        # 5) Devolver métricas y flags
        return {
            "ear": ear,
            "eyes_closed": self.is_closed,
            "drowsy": self.in_drowsy_state,
            "should_beep": should_beep,
        }

    def mark_alert_played(self):
        """
        Marcar que la alarma se ha reproducido: forzar el cooldown completo.
        Llamar desde el código que efectivamente reproduce el sonido para sincronizar.
        """
        self.cooldown = self.cooldown_seconds