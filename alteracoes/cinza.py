import cv2

def apply_cinza(img, params=None):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)