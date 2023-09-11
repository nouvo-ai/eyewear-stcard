import subprocess
import cv2
import numpy as np

# Run the first script to create the first combined image
subprocess.run(['python', 'combine_images_1.py'])

# Run the second script to create the second combined image
subprocess.run(['python', 'combine_images_2.py'])

# Load the card image
card = cv2.imread('srcs/card.png')
card2 = np.copy(card)

# Load the first and second combined images
combined_image_1 = cv2.imread('output/output_1.png')
combined_image_2 = cv2.imread('output/output_2.png')

# Paste the first combined image on the card image at (156, 156)
card[156:156+combined_image_1.shape[0], 156:156+combined_image_1.shape[1]] = combined_image_1

# Paste the second combined image on the card image at (156, 156)
card2[156:156+combined_image_2.shape[0], 156:156+combined_image_2.shape[1]] = combined_image_2

# Save the final result
cv2.imwrite('output/output_3.png', card)
cv2.imwrite('output/output_4.png', card2)
