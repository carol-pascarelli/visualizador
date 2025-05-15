import cv2

def apply_contraste(img, params=None):
    alpha = 1.5  # intensidade
    beta = 0     # brilho
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
