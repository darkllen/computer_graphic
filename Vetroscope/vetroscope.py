import cv2
import numpy as np
from sys import argv
#709
src = cv2.imread('original.tif')

#get bgr
B, G, R = src[:,:,0], src[:,:,1], src[:,:,2]

#convert to YCC 709 according to presentation
Y = (0.299 * R) + (0.587 * G) + (0.114 * B) 
Cb = (-0.169 * R) - (0.331 * G) + (0.5 * B) +128
Cr = (0.5 * R) - (0.418 * G) - (0.082 * B) + 128
Cr = 256 - Cr

#make vetroscope
dst = np.zeros((256, 256, 3))
for x in range(src.shape[0]):
  for y in range(src.shape[1]):
    dst[int(Cr[x, y]), int(Cb[x, y])] = np.array([B[x, y], G[x, y], R[x, y]])
cv2.imwrite('vetroscope.jpg', dst)

#convert to YCC with cv2
YCrCbImage = cv2.cvtColor(src, cv2.COLOR_BGR2YCrCb)
cv2.imwrite('YCbCr_cv2.jpg', YCrCbImage)

#convert to YCC with cv2 formuls
Cr2 = (R-Y)*0.713+128
Cb2 = (B-Y)*0.564+128

img = np.zeros([1984,2128,3])
img [:,:,0] = Y
img [:,:,1] = Cb2
img [:,:,2] = Cr2
cv2.imwrite('my_as_cv2.jpg', img)

img [:,:,0] = Y
img [:,:,1] = Cb
img [:,:,2] = Cr
cv2.imwrite('my_as_lection.jpg', img)

#convert back (wiki and cv2 formuls same)
R = Y+1.403 * (Cr2-128)
G = Y - 0.714 * (Cr2 - 128) - 0.344 * (Cb2 - 128)
B = Y + 1.773 * (Cb2 - 128)

img [:,:,0] = B
img [:,:,1] = G
img [:,:,2] = R

cv2.imwrite('my_back_as_cv2.jpg', img)

R = Y+1.403 * (Cr-128)
G = Y - 0.714 * (Cr - 128) - 0.344 * (Cb - 128)
B = Y + 1.773 * (Cb - 128)

img [:,:,0] = B
img [:,:,1] = G
img [:,:,2] = R

cv2.imwrite('my_back_as_lection.jpg', img)