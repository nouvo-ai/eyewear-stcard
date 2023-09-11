import cv2
import numpy as np

# Load the images with alpha channel
test_ytt_model = cv2.imread('srcs/test_ytt_model.png', cv2.IMREAD_UNCHANGED)
test_ytt = cv2.imread('srcs/test_ytt.png', cv2.IMREAD_UNCHANGED)

# Ensure that the images have the same size
test_ytt = cv2.resize(test_ytt, (test_ytt_model.shape[1], test_ytt_model.shape[0]))

# Create a mask using the alpha channel of test_ytt
mask = test_ytt[:, :, 3]

# Merge the two images considering the alpha channel
combined_image = np.copy(test_ytt_model)

for c in range(0, 3):
    combined_image[:, :, c] = test_ytt[:, :, c] * (test_ytt[:, :, 3] / 255.0) + combined_image[:, :, c] * (1.0 - test_ytt[:, :, 3] / 255.0)

# Save the result
cv2.imwrite('output/output_1.png', combined_image)
