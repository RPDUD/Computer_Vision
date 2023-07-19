import cv2
import numpy as np
from skimage.filters import threshold_local
import tensorflow as tf
from skimage import measure
import imutils

def sort_cont(character_contours):
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in character_contours]
    (character_contours, boundingBoxes) = zip(*sorted(zip(character_contours, boundingBoxes),
                                                      key=lambda b: b[1][i], reverse = False))
    return character_contours

def segment_chars(plate_img, fixed_width):
    V = cv2.split(cv2.cvtColor(plate_img, cv2.COLOR_BGR2HSV))[2]
    T = threshold_local(V, 29, offset=15, method='gaussian')
    
    thresh = (V > T).astype('uint8') * 255
    
    thresh = cv2.bitwise_not(thresh)
    
    plate_img = imutils.resize(plate_img, width = fixed_width)
    thresh = imutils.resize(thresh, width = fixed_width)
    bgr_thresh = cv2.color(thresh, cv2.COLOR_GRAY2BGR)
    
    labels = measure.label(thresh, neighbors = 8, background = 0)
    
    charCandinates = np.zeros(thresh.shape, dtype = 'uint8')
    
    characters = []
    
    for label in np.unique(labels):
        if label == 0:
            continue
        
        labelMask - np.zeros(thresh.shape, dtype = 'uint8')
        labelMask[labels == label] = 255
        
        cnts = cv2.findContours(labelMAsk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        
        if len(cnts) > 0:
            c = max(cnts, key = cv2.contourArea)
            (boxX, boxY, boxW, boxH) = cv2.boundingRect(c)
            
            aspectRatio = boxW/float(boxH)
            solidity = cv2.contourArea(c)/float(boxW*boxH)
            heightRatio = boxH/float(plate_img.shape[0])
            
            keepAspectRatio = aspectRatio < 1.0
            keepSolidity = solidity > 0.15
            keepHeight = height > 0.5 and heightRatio < 0.95
            
            if keepAspectRatio and keepSolidity and keepHeight and boxW > 14:
                hull = cv2.convexHull(c)
                            