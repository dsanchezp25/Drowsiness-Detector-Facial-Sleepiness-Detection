import cv2
import mediapipe as mp

class FaceMeshDetector:
    def __init__(self,
                 max_faces = 1,
                 min_detection_confidence = 0.5,
                 min_tracking_confidence = 0.5):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces = max_faces,
            refine_landmarks = True,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence
        )
        self.result = None
        self.last_landmarks = None

        # para dibujar
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles

    def process(self, frame_bgr):
        # mediapipe trabaja con rgb
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        self.result = self.face_mesh.process(frame_rgb)

        if self.result.multi_face_landmarks:
            # solo una cara
            self.last_landmarks = self.result.multi_face_landmarks[0].landmark
            return self.last_landmarks
        else:
            self.last_landmarks = None
            return None

    def draw_landmarks(self, frame_bgr):
        if not self.result or not self.result.multi_face_landmarks:
            return

        for face_landmarks in self.result.multi_face_landmarks:
            self.mp_drawing.draw_landmarks(
                image = frame_bgr,
                landmark_list = face_landmarks,
                connections = self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec = None,
                connection_drawing_spec = self.mp_styles.get_default_face_mesh_tesselation_style()
            )
