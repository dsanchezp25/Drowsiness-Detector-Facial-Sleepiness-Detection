import cv2

def draw_status_banner(frame, text, top=10):
    h, w, _ = frame.shape
    pad = 6
    (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
    cv2.rectangle(frame, (8, top-24), (8 + text_w + 2*pad, top + text_h + 2*pad), (0, 0, 0), -1)
    cv2.putText(frame, text, (8 + pad, top + text_h), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

def draw_drowsy(frame):
    cv2.putText(frame, "DROWSINESS DETECTED", (50,80), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0,0,255), 3)

def draw_yawn(frame):
    cv2.putText(frame, "ALERT! WAKE UP!", (50,130), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 3)