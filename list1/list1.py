import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

ball_img = cv.imread("./Bola.jpg")
colored_lena = cv.imread("./LenaC.jpg")
black_white_lena = cv.imread("./LenaPB.jpg")


# 1)
cv.imshow("Show image", ball_img)
cv.waitKey(10000)

output_dir = "./image_saved"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
cv.imwrite("./image_saved/ball_saved.jpg", ball_img)



# 2)
img_turned_grey = cv.cvtColor(colored_lena, cv.COLOR_BGR2GRAY)
cv.imshow("Colored image turned grey", img_turned_grey)
cv.waitKey(10000)



# 3)
blue_channel = colored_lena[:, :, 0]
green_channel = colored_lena[:, :, 1]
red_channel = colored_lena[:, :, 2]

blue_image = np.zeros_like(colored_lena)
blue_image[:, :, 0] = blue_channel

green_image = np.zeros_like(colored_lena)
green_image[:, :, 1] = green_channel

red_image = np.zeros_like(colored_lena)
red_image[:, :, 2] = red_channel

cv.imwrite("./image_saved/blue_channel.jpg", blue_image)
cv.imwrite("./image_saved/green_channel.jpg", green_image)
cv.imwrite("./image_saved/red_channel.jpg", red_image)

cv.imshow("Colored image", colored_lena)
cv.waitKey(10000)



# 4)
img_turned_grey = cv.cvtColor(colored_lena, cv.COLOR_BGR2GRAY)
cv.imshow("Colored image turned grey 2", img_turned_grey)
cv.waitKey(10000)

blurred_image = cv.blur(img_turned_grey, (7, 7))
cv.imshow("Mean blurred image", blurred_image)
cv.imwrite("./image_saved/mean_blurred.jpg", blurred_image)
cv.waitKey(10000)

median_blurred_image = cv.medianBlur(img_turned_grey, 7)
cv.imshow("Median blurred image", median_blurred_image)
cv.imwrite("./image_saved/median_blurred.jpg", median_blurred_image)
cv.waitKey(10000)



# 5)
img_turned_grey = cv.cvtColor(colored_lena, cv.COLOR_BGR2GRAY)
cv.imshow("Colored image turned grey 3", img_turned_grey)
cv.waitKey(10000)
thresholded_image = np.zeros_like(img_turned_grey)
for i in range(img_turned_grey.shape[0]):
    for j in range(img_turned_grey.shape[1]):
        if img_turned_grey[i][j] > 80:
            thresholded_image[i][j] = 255
        else:
            thresholded_image[i][j] = 0
cv.imshow("Thresholded image", thresholded_image)
cv.imwrite("./image_saved/thresholded_image.jpg", thresholded_image)
cv.waitKey(10000)



# 6)
img_turned_grey = cv.cvtColor(colored_lena, cv.COLOR_BGR2GRAY)
cv.imshow("Colored image turned grey 4", img_turned_grey)
cv.waitKey(10000)

grey_histogram = cv.calcHist([img_turned_grey], [0], None, [256], [0, 256])

plt.figure(figsize=(6, 4))
plt.plot(grey_histogram)
plt.title('Histogram of Grayscale Image')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')
plt.xlim(0, 256)
plt.show()



equalized_img = cv.equalizeHist(img_turned_grey)
cv.imshow('Equalized Image', equalized_img)
cv.waitKey(10000)

equalized_histogram = cv.calcHist([equalized_img], [0], None, [256], [0, 256])

plt.figure(figsize=(6, 4))
plt.plot(equalized_histogram)
plt.title('Histogram of Equalized Grayscale Image')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')
plt.xlim(0, 256)
plt.show()

cv.imwrite("./image_saved/equalized_image.jpg", equalized_img)

cv.destroyAllWindows()