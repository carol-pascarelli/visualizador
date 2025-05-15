import cv2

def apply_rotacionar(img, params):
    try:
        angle = float(params) if params else 90
    except ValueError:
        angle = 90

    # Pega o centro da imagem
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)

    # Gera matriz de rotação e aplica
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, matrix, (w, h))

    return rotated
