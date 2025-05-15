import cv2

def apply_blur(img, params=None):
    return cv2.GaussianBlur(img, (5, 5), 0)
