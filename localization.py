import cv2
import numpy as np
import localization_helpers
import tensorflow as tf


def localize(img):
    # resizes image if height or width are larger than 1280px
    if img.shape[0] > 1280 or img.shape[1] > 1280:
        img = tf.image.resize(img, (1280, 1280), method="bilinear", preserve_aspect_ratio=True)
    # converts image to B/W, blurs it and applies thresholding
    gray = cv2.cvtColor(np.float32(img), cv2.COLOR_BGR2GRAY)
    brightness = localization_helpers.automatic_brightness_and_contrast(gray, clip_hist_percent=0.1)
    blur = cv2.GaussianBlur(brightness, (5, 5), cv2.BORDER_DEFAULT)
    thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV)[1]


    # finds only external contours (to help with closed digits) and sorts by x coordinate
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    char_photos_inter = list()
    char_photos = list()
    rect_areas = list()
    # draws rectangles around contours while storing each characters' coordinates and photos
    for ctr in sorted_contours:
        x, y, w, h = cv2.boundingRect(ctr)
        rect_areas.append(h * w)
        char_photos_inter.append(brightness[y:y + h, x:x + w])
        
    median_rect_area = np.median(rect_areas)
    # tries to delete very small contours which shouldn't belong to characters
    for i, ctr in enumerate(sorted_contours):
        if rect_areas[i] > median_rect_area * 0.1:
            char_photos.append(char_photos_inter[i])
    return char_photos
