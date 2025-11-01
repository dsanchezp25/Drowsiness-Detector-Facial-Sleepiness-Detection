import sys

def play_alert(frequency: int = 1000, duration_ms: int = 200):
    """
    Reproduce una alerta sonora.
    - frequency: frecuencia en Hz (por defecto 1000).
    - duration_ms: duración en milisegundos (por defecto 200).
    Esta función mantiene compatibilidad con llamadas sin argumentos.
    """
    print("[ALERT] play_alert called")
    try:
        # Comprobar si la plataforma es Windows (winsound está disponible ahí)
        if sys.platform.startswith("win"):
            import winsound  # import local para evitar errores en otras plataformas
            # winsound.Beep(frequency, duration_ms) reproduce un beep (blocking)
            winsound.Beep(frequency, duration_ms)
        else:
            # En otras plataformas no hay implementación de beep aquí;
            # se deja un mensaje como fallback; se puede ampliar para usar pydub/pygame, etc.
            print("[ALERT] BEEP (no win)")
    except Exception as e:
        # Registrar el error sin lanzar para no romper el flujo de detección visual
        print(f"[ALERT] Could not beep: {e}")