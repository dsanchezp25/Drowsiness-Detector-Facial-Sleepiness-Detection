import cv2  # OpenCV: captura de cámara y operaciones sobre imágenes
import mediapipe as mp  # MediaPipe: detector de malla facial y utilidades de dibujo

class FaceMeshDetector:
    """
    Encapsula la lógica de MediaPipe Face Mesh:
    - Inicializa el modelo con parámetros configurables.
    - Procesa frames BGR y devuelve landmarks normalizados.
    - Dibuja la malla sobre un frame BGR cuando se solicita.
    """

    def __init__(self,
                 max_faces = 1,
                 min_detection_confidence = 0.5,
                 min_tracking_confidence = 0.5):
        # Guardar referencias a módulos de MediaPipe para uso posterior
        self.mp_face_mesh = mp.solutions.face_mesh

        # Inicializar la solución FaceMesh de MediaPipe
        # - max_num_faces: número máximo de caras a detectar
        # - refine_landmarks: mejora la localización de puntos alrededor de los ojos/labios
        # - min_detection_confidence / min_tracking_confidence: umbrales para detección/seguimiento
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces = max_faces,
            refine_landmarks = True,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence
        )

        # Resultado de la última inferencia de MediaPipe (objeto complejo)
        self.result = None
        # Lista de landmarks (normalizados) de la última cara detectada o None
        self.last_landmarks = None

        # Utilidades para dibujar (drawing-utils y estilos de MediaPipe)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles

    def process(self, frame_bgr):
        """
        Procesa un frame BGR y devuelve la lista de landmarks de la primera cara detectada.
        - Convierte BGR -> RGB porque MediaPipe espera RGB.
        - Llama a self.face_mesh.process y almacena el resultado.
        - Si hay caras detectadas, guarda y retorna los landmarks de la primera.
        - Si no, limpia el estado y retorna None.
        """
        # MediaPipe trabaja con imágenes RGB
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        # Ejecutar la detección/seguimiento de Face Mesh
        self.result = self.face_mesh.process(frame_rgb)

        # Si se detectaron landmarks de una o más caras, usar la primera (solo 1 por defecto)
        if self.result.multi_face_landmarks:
            # multi_face_landmarks es una lista; cada elemento tiene .landmark (lista normalizada)
            self.last_landmarks = self.result.multi_face_landmarks[0].landmark
            return self.last_landmarks
        else:
            # No se detectó cara: limpiar estado y devolver None
            self.last_landmarks = None
            return None

    def draw_landmarks(self, frame_bgr):
        """
        Dibuja la malla facial sobre el frame BGR usando los estilos por defecto.
        - No hace nada si no hay resultado o no hay caras detectadas.
        - Recorre cada cara detectada y dibuja conexiones según FACEMESH_TESSELATION.
        """
        if not self.result or not self.result.multi_face_landmarks:
            # Nada que dibujar
            return

        for face_landmarks in self.result.multi_face_landmarks:
            # Dibujar landmarks y conexiones en el frame BGR
            self.mp_drawing.draw_landmarks(
                image = frame_bgr,
                landmark_list = face_landmarks,
                connections = self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec = None,  # usar estilos por defecto para puntos
                connection_drawing_spec = self.mp_styles.get_default_face_mesh_tesselation_style()
            )