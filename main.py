import cv2  # OpenCV: captura de cámara y manejo de imágenes

from config import *  # Carga constantes de configuración (índice de cámara, umbrales, flags)
from detectors.face_mesh_detector import FaceMeshDetector  # Detector de malla facial (landmarks)
from detectors.drowiness_analyzer import DrowsinessAnalyzer  # Lógica para calcular EAR y somnolencia
from alerts.visual_alert import draw_status_banner, draw_drowsy  # Funciones para dibujar alertas en el frame
from alerts.sound_alert import play_alert  # Reproducir sonido de alerta (pydub/ffmpeg)

def main():
    # Abrir la cámara con el índice configurado
    cap = cv2.VideoCapture(CAMARA_INDEX)
    if not cap.isOpened():
        # Si no se pudo abrir la cámara, salir
        print("Error al abrir la cámara")
        return

    # Inicializar detector de landmarks y analizador de somnolencia con los umbrales de configuración
    detector = FaceMeshDetector()
    analyzer = DrowsinessAnalyzer(
        ear_threshold = EAR_THRESHOLD,
        closed_seconds = CLOSED_SECONDS,
    )

    prev_drowsy = False  # Estado previo de somnolencia (puede usarse para evitar repetición de alertas)

    while True:
        # Leer un frame de la cámara
        ret, frame = cap.read()
        if not ret:
            # Si falla la lectura, terminar el bucle
            print("Error al leer el frame")
            break

        # Procesar el frame para obtener landmarks faciales (o None si no se detecta cara)
        landmarks = detector.process(frame)

        if landmarks is not None:
            # Si está activada la opción, dibujar la malla facial sobre el frame
            if SHOW_MESH:
                detector.draw_landmarks(frame)

            # Analizar landmarks para obtener métricas (ej. EAR) y flags (ojos cerrados, somnoliento, debe sonar)
            result = analyzer.analyze(landmarks, frame.shape)
            ear = result["ear"]

            # Mostrar el valor EAR en la esquina superior izquierda
            cv2.putText(frame, f"EAR: {result['ear']:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Si los ojos están cerrados, mostrar una banda indicadora
            if result["eyes_closed"]:
                draw_status_banner(frame, "Eyes Closed", top = 95)

            # Si el analizador determina somnolencia, dibujar alerta visual
            if result["drowsy"]:
                draw_drowsy(frame)
                # Si además indica que debe sonar la alarma, reproducir sonido y marcar que ya sonó
                if result["should_beep"]:
                    print("Drowsiness detected! Playing alert.")
                    play_alert()
                    analyzer.mark_alert_played()

        # Mostrar el frame procesado en una ventana llamada "Frame"
        cv2.imshow("Frame", frame)
        # Salir al pulsar la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos: cámara y ventanas de OpenCV
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()