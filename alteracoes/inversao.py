import cv2

def apply_inversao(img, params=None):
    return cv2.bitwise_not(img)
