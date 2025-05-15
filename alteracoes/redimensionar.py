import cv2

def apply_redimensionar(img, params):
    try:
        # Aceita: "300x400" ou "0.5" (escala)
        if "x" in params.lower():
            width, height = map(int, params.lower().split("x"))
            resized = cv2.resize(img, (width, height))
        else:
            scale = float(params)
            resized = cv2.resize(img, (0, 0), fx=scale, fy=scale)
        return resized
    except Exception:
        # Padrão caso erro: reduz 50%
        return cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
