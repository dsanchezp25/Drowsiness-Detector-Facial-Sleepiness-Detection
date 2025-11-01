# 😴 Drowsiness-Detector-Facial-Sleepiness-Detection  ![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python) ![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv) ![MediaPipe](https://img.shields.io/badge/MediaPipe-latest-orange) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🎬 Descripción del Proyecto

**Drowsiness-Detector-Facial-Sleepiness-Detection** es una herramienta en **Python** que utiliza **OpenCV** y **MediaPipe Face Mesh** para detectar en tiempo real señales de somnolencia mediante la webcam. Analiza *landmarks* faciales (ojos, boca y cabeza) para detectar ojos cerrados y bostezos, y emite alertas visuales y sonoras cuando detecta fatiga.

---

## 🧠 Tecnologías Utilizadas

- 🐍 **Python 3.8+**
- 🧮 **NumPy**
- 👁️ **OpenCV**
- 🧭 **MediaPipe Face Mesh**

---

## ⚙️ Instalación y Ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/dsanchezp25/drowsiness-detector.git
cd drowsiness-detector
```

### 2️⃣ Crear y activar entorno virtual (Windows)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar
```bash
python main.py
```
Presiona `q` o usa **Ctrl+C** para salir.

---

## 📁 Archivos clave

| Archivo / Módulo | Descripción |
| ---------------- | ----------- |
| `main.py` | Punto de entrada: captura cámara, bucle principal y gestión de alertas. |
| `detectors/face_mesh_detector.py` | Encapsula MediaPipe Face Mesh y entrega landmarks normalizados. |
| `detectors/drowsiness_analyzer.py` | Lógica de detección basada en EAR, temporización y cooldown. |
| `metrics/eye_metrics.py` | Cálculo de Eye Aspect Ratio (EAR) y utilidades para landmarks. |
| `alerts/visual_alert.py` | Dibujo de banners y avisos en el frame. |
| `alerts/sound_alert.py` | Reproducción de alerta sonora (Windows: `winsound`, fallback en otros SO). |
| `requirements.txt` | Dependencias del proyecto. |
| `README.md` | Documentación (este archivo). |

---

## 🧩 Funcionamiento Interno

### 1) Captura y preprocesado
- `main.py` captura frames BGR de la webcam y los envía al detector.
- Para rendimiento se recomienda reducir resolución o usar un `DETECT_SCALE`.

### 2) Detección de landmarks
- `detectors/face_mesh_detector.py` convierte BGR → RGB y llama a MediaPipe.
- Devuelve landmarks normalizados por cara detectada.

### 3) Cálculo de métricas
- `metrics/eye_metrics.py` transforma landmarks a coordenadas de píxeles y calcula EAR para cada ojo.
- También puede calcular apertura de boca para detectar bostezos.

### 4) Análisis temporal
- `detectors/drowsiness_analyzer.py` compara EAR con `ear_threshold`.
- Si los ojos permanecen por debajo del umbral durante `closed_seconds`, se declara somnolencia.
- `cooldown_seconds` evita alarmas repetidas.

### 5) Alertas
- `alerts/visual_alert.py` dibuja banners y mensajes en el frame.
- `alerts/sound_alert.py` intenta reproducir beep en Windows con `winsound.Beep`; en otros SO muestra fallback o puede reproducir archivo si se integra audio adicional.

---

## 🎛️ Parámetros importantes

| Parámetro | Descripción | Valor por defecto |
| --------- | ----------- | ----------------- |
| `ear_threshold` | Umbral EAR para considerar ojo cerrado | `0.38` |
| `closed_seconds` | Segundos continuos de ojos cerrados para declarar somnolencia | `1.0` |
| `cooldown_seconds` | Tiempo mínimo entre alarmas sonoras | `1.0` |
| `DETECT_SCALE` | Factor para reducir la imagen antes de detectar (rendimiento) | `0.5` |
| `CAM_INDEX` | Índice o URL de la fuente de vídeo | `0` (cámara principal) |

> 🔧 Ajustar `ear_threshold` y `closed_seconds` según la cámara, distancia y sujeto para reducir falsos positivos.

---

## 🧰 Solución de Problemas

| Problema | Solución |
| -------- | ------- |
| 📷 Cámara no detectada | Verificar permisos de cámara y que no esté en uso por otra app. |
| ❌ MediaPipe falla al importar | Comprobar versión de `mediapipe` y compatibilidad con plataforma/Python. |
| 🔕 No suena la alarma en macOS/Linux | `alerts/sound_alert.py` usa `winsound` en Windows; integrar `pygame` o `simpleaudio` para multiplataforma. |
| 🐢 Bajos FPS | Reducir `DETECT_SCALE` o bajar resolución de la cámara. |
| ⚠️ Falsas alarmas | Calibrar `ear_threshold` y aumentar `closed_seconds`. |

---

## 🧩 Pruebas

- Es recomendable crear tests unitarios para:
  - `metrics/eye_metrics.py` (cálculo de distancias y EAR).
  - `detectors/drowsiness_analyzer.py` (simulación de tiempos y cooldown).
- Ejecutar con `pytest` si se incluye la carpeta `tests/`.

---

## 🌟 Mejoras Futuras

- Sustituir MediaPipe por modelos DNN o técnicas más robustas para mayor precisión.
- Detectar y gestionar múltiples caras simultáneamente.
- Añadir calibración interactiva (trackbars) para `ear_threshold` y tiempos.
- Reproducción de audio multiplataforma y uso de sonidos personalizados.
- Registro de eventos y exportación de métricas a CSV/JSON.

## ✍️ Autor

**Daniel Sánchez Parra** (dsanchezp25)  
Repositorio y issues en GitHub: `https://github.com/dsanchezp25/drowsiness-detector`

---
```