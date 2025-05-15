import cv2

def apply_sharpen(img, params=None):
    return cv2.addWeighted(img, 1.5, cv2.GaussianBlur(img, (0, 0), 3), -0.5, 0)
