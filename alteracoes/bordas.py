import cv2

def apply_bordas(img, params=None):
    return cv2.Canny(img, 100, 200)
