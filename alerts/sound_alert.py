import sys

def play_alert():
    """
        Intenta un beep simple en Windows; en otros sistemas
        intenta simpleaudio si está instalado.
    """

    try:
        if sys.platform.startswith("win"):
            import winsound
            winsound.Beep(1000, 400)  # frecuencia 1000Hz, duración 400ms

    except Exception:
        # fallback silencioso si no se puede reproducir
        pass
