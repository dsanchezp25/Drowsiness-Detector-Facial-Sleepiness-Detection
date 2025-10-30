import cv2

from config import *
from detectors.face_mesh_detector import FaceMeshDetector
from detectors.drowiness_analyzer import DrowinessAnalyzer
from metrics.eye_metrics import compute_average_ear
from alerts.visual_alert import draw_status_banner, draw_drowsy, draw_yawn
from alerts.sound_alert import play_alert

def main():
    cap = cv2.VideoCapture(CAMARA_INDEX)
    if not cap.isOpened():
        print("Error al abrir la cámara")
        return

    detector = FaceMeshDetector()
    analyzer = DrowinessAnalyzer(
        ear_threshold=EAR_THRESHOLD,
        frames_threshold=FRAMES_THRESOLD,
        mar_threshold=MAR_THRESHOLD,
        yawn_frames_threshold=YAWN_FRAMES_THRESHOLD
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al leer el frame")
            break

        # Procesar el frame
        landmarks = detector.process(frame)

        if landmarks is not None:
            if SHOW_MESH:
                detector.draw_landmarks(frame)

            result = analyzer.analyze(landmarks, frame.shape)

            #pintar valor
            cv2.putText(frame, f"EAR: {result['ear']:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, f"MAR: {result['mar']:.2f}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            if result["yawn"]:
                draw_yawn(frame)

            if result["drowsy"]:
                draw_drowsy(frame)
                if result["should_beep"]:
                    play_alert()
                    analyzer.mark_alert_played()

            if result["eyes_closed"]:
                draw_status_banner(frame, "Eyes Closed", top = 95)


        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()