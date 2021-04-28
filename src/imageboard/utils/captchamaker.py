import random
import base64
import io
import hashlib
import os

import PIL
from PIL import Image, ImageFont, ImageDraw

from imageboard.utils.wakabawords import make_word


COLOR_MODE = 'RGBA'
BACKGROUND_COLOR = (255, 255, 255, 0)  # Transparent white
MAIN_COLOR = (0, 0, 0, 255)  # Solid black
TRANSPARENT_COLOR = (0, 0, 0, 0)  # Transparent black

FONT_SIZE = 20
VERTICAL_LETTER_CROP = 7

CAPTCHA_WIDTH = 128
CAPTCHA_HEIGHT = 32

HORIZONTAL_SHIFT_RATIO = 0.5
HORIZONTAL_PADDING = 10
MAX_VERTICAL_SHIFT = 5
VERTICAL_PADDING = int((CAPTCHA_HEIGHT - FONT_SIZE) / 2)


# Load font object
module_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(module_dir, 'OpenSans-Light.ttf'), 'rb') as f:
    font = PIL.ImageFont.truetype(font=f, size=FONT_SIZE)


def draw_distored_text(image, text, left, top):
    # Text angle can be random in specified alternating ranges
    angle_ranges = [(-30, -15), (15, 30)]
    current_angle_range = 0

    # Intial character coordinates
    x = left + HORIZONTAL_PADDING
    padded_top = top + VERTICAL_PADDING
    y = padded_top

    # Draw text string char by char
    for char in text:
        # Get char dimensions
        char_width, char_height = font.getsize(char)

        # Create new image for char
        new_image = Image.new(COLOR_MODE, (char_width, char_height), TRANSPARENT_COLOR)

        # Draw text on the char image
        new_surface = PIL.ImageDraw.Draw(new_image)
        new_surface.text(xy=(0, 0), text=char, fill=MAIN_COLOR, font=font)

        # Crop image at the top because font leaves too much space
        new_image = new_image.crop((0, VERTICAL_LETTER_CROP, new_image.width, new_image.height))

        # Rotate char image, with special handling for 'I' and 'J'
        random_angle = random.randint(*angle_ranges[current_angle_range])
        new_image = new_image.rotate(random_angle, expand=True, resample=PIL.Image.BICUBIC)

        # Paste char image to the base one, shift it to the left a little to overlap chars
        x_shift = int(new_image.width * HORIZONTAL_SHIFT_RATIO)
        image.alpha_composite(new_image, (max(0, x - x_shift), y))

        # Increment horizontal offset (width with shift)
        x += int(new_image.width - x_shift)

        # Randomize vertical offset
        y = padded_top + random.randint(-MAX_VERTICAL_SHIFT, MAX_VERTICAL_SHIFT)

        # Switch angle range
        current_angle_range = 0 if current_angle_range == 1 else 1


def draw_test_sheet():
    image = PIL.Image.new(COLOR_MODE, (1920, 1080), BACKGROUND_COLOR)
    image_surface = PIL.ImageDraw.Draw(image)

    for x_num in range(10):
        for y_num in range(20):
            # Generate captcha word
            solution = make_word().upper()

            # Draw captcha word
            draw_distored_text(image, solution, x_num * CAPTCHA_WIDTH, y_num * CAPTCHA_HEIGHT)

            # Draw a border around captcha
            image_surface.rectangle(
                [
                    x_num * CAPTCHA_WIDTH, y_num * CAPTCHA_HEIGHT,
                    (x_num + 1) * CAPTCHA_WIDTH, (y_num + 1) * CAPTCHA_HEIGHT,
                ],
                outline=MAIN_COLOR,
                fill=None
            )

    image.show()


def draw_single_captcha(solution, image_size=(CAPTCHA_WIDTH, CAPTCHA_HEIGHT)):
    image = PIL.Image.new(COLOR_MODE, image_size, BACKGROUND_COLOR)
    draw_distored_text(image, solution, 0, 0)
    return image


def image_to_bytes(image):
    bytes_virtual_file = io.BytesIO()
    image.save(bytes_virtual_file, format='PNG')
    image_bytes = bytes_virtual_file.getvalue()
    return image_bytes


def image_to_base64(image):
    image_bytes = image_to_bytes(image)
    image_base64 = 'data:image/png;base64,' + base64.b64encode(image_bytes).decode('ascii')
    return image_base64


def make_captcha_create_kwargs():
    solution = make_word().upper()
    image = draw_single_captcha(solution)
    image_base64 = image_to_base64(image)
    return {
        'solution': solution,
        'image': image_base64,
    }


if __name__ == '__main__':
    draw_test_sheet()
