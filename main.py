# exlib
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
# stdlib
import random
# userlib
import const

# Merge the two images considering the alpha channel
def add_glasses(model:np.ndarray, glasses:np.ndarray) -> np.ndarray:
    # Ensure that the images have the same size
    glasses = cv2.resize(glasses, (model.shape[1], model.shape[0]))

    combined_image = np.copy(model)
    for c in range(0, 3):
        combined_image[:, :, c] = glasses[:, :, c] * (glasses[:, :, 3] / 255.0) + combined_image[:, :, c] * (1.0 - glasses[:, :, 3] / 255.0)
    return combined_image

# Paste the combined_image on the card image at (156, 156)
def photo_to_id_card(photo:np.ndarray, id_card:np.ndarray) -> np.ndarray:
    id_card[156:156+photo.shape[0], 156:156+photo.shape[1]] = photo
    return id_card

def text_to_id_card(id_card:Image, id_card_info:dict, optical_num:int) -> Image:
    Unica77_path = "fonts/Unica77LL-Regular.otf"
    Noto_Sans_path = "fonts/NotoSans-Regular.ttf"
    font_size = 84
    font_color = "#781945"
    letter_spacing = 1
    is_en = id_card_info["is_en"]
    # name = id_card_info["name"]
    name = const.MODEL_NAME[optical_num]
    optical_id = const.OPTICAL_MODEL_NAME[optical_num]

    # validate string
    font = ImageFont.truetype(Unica77_path, font_size)
    if not is_en:
        font = ImageFont.truetype(Noto_Sans_path, font_size)

    # draw text
    draw = ImageDraw.Draw(id_card)
    x1, y1 = 153, 1509
    draw.text((x1, y1), name, fill=font_color, font=font, spacing=letter_spacing, anchor="ls")
    x2, y2 = 153, 1718
    draw.text((x2, y2), optical_id, fill=font_color, font=font, spacing=letter_spacing, anchor="ls")

    return id_card

if __name__ == "__main__":
    # input data
    id_card_info = {
        "name": "TEST",
        "is_en": True,
        "sex": "male",
    }

    if id_card_info["sex"] == "female":
        optical_num = random.randint(1, 4)
    elif id_card_info["sex"] == "male":
        optical_num = random.randint(5, 8)
    else:
        optical_num = random.choice([1, 4, 6, 7])

    # add_glasses() usage
    test_ytt_model = cv2.imread(f'srcs/model_{optical_num:02}.png', cv2.IMREAD_UNCHANGED)
    test_ytt = cv2.imread(f'srcs/atomic_{optical_num:02}.png', cv2.IMREAD_UNCHANGED)
    # test_ytt = cv2.imread('srcs/test_ytt_x3.png', cv2.IMREAD_UNCHANGED)
    combined_image = add_glasses(test_ytt_model, test_ytt)
    cv2.imwrite('output/combined_image.png', combined_image)

    # photo_to_id_card() usage
    id_card = cv2.imread('srcs/card.png')
    photo = cv2.imread('output/combined_image.png')
    id_card = photo_to_id_card(photo, id_card)
    cv2.imwrite('output/id_card.png', id_card)

    # text_to_id_card() usage
    id_card_image_path = "output/id_card.png"
    id_card = Image.open(id_card_image_path)
    result_image = text_to_id_card(id_card, id_card_info, optical_num)
    # result_image.show()
    result_image.save('output/student_id_card.png')