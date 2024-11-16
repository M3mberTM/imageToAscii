from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import cv2 as cv
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import math


#  $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.
#  .-;+=xX$█
#  █$Xx=+;-.

# C:\\Users\\risko\\Documents\\Pictures\\cyberpunkGasMask.png
# ./images/blank_white.png

# TODO better name methods
# TODO add comments around for better understanding of code later
class ImageAsciiGenerator:
    ascii_gradient = " .-;+=xX$█"
    test_file_path = "./testImages/cyberpunkGasMask.png"  # test image size 1664 x 1664
    TEST = False
    filename = ""
    image_dimensions = None
    text_size = 16
    width_divisor = float
    height_divisor = float
    # monospace fonts: consolaz, cour, lucon
    text_font = ImageFont.truetype("lucon.ttf", text_size)
    bloom = bool

    def get_ascii_index_value(self, brightness: float):
        divider = 255 / (len(self.ascii_gradient) - 1)
        return int(brightness // divider)

    def __init__(self, font_size: int, ascii_gradient: str, bloom: bool):
        if not self.TEST:
            Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
            self.filename = askopenfilename()
            self.text_size = font_size
            self.ascii_gradient = ascii_gradient
            self.text_font = ImageFont.truetype("lucon.ttf", self.text_size)
        else:
            self.filename = self.test_file_path
        self.width_divisor = self.text_size / 0.84
        self.height_divisor = self.width_divisor / 1.5
        self.bloom = bloom

    def load_image(self) -> list[list]:
        img = cv.imread(self.filename, cv.IMREAD_COLOR)
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        self.image_dimensions = np.shape(img)

        new_width = math.floor(self.image_dimensions[1] / self.width_divisor)
        new_height = math.floor(self.image_dimensions[0] / self.height_divisor)
        resized_img = cv.resize(img, (new_width, new_height))
        return resized_img

    def pixels_to_text(self, resized_img) -> str:
        ascii_img = ""

        for i in range(len(resized_img)):
            for j, k in enumerate(resized_img[i]):
                current_char = self.ascii_gradient[self.get_ascii_index_value(k[2])]
                ascii_img = ascii_img + current_char + current_char
            ascii_img = ascii_img + "\n"
        return ascii_img

    def draw_text_on_img_adjusted(self, text: str, background_color: tuple, text_color: tuple):
        width_tolerance = 1.05  # scales the image slightly to take into account the lost accuracy with flooring later
        height_tolerance = 1.1
        im = Image.new(mode="RGB", size=(math.floor(self.image_dimensions[1] * width_tolerance), math.floor(self.image_dimensions[0] * height_tolerance)), color=background_color)
        draw = ImageDraw.Draw(im)
        text_lines = text.split("\n")
        # the last line is just an empty string due to the \n character being at the end
        for i in range(len(text_lines)-2):
            for j, char in enumerate(text_lines[i]):
                gradient_length = len(self.ascii_gradient)
                current_char_position = self.ascii_gradient.index(char)
                divisor = math.floor((current_char_position / gradient_length)*10) / 10
                char_color = (math.floor(text_color[0] * divisor), math.floor(text_color[1] * divisor), math.floor(text_color[2] * divisor))
                x = math.ceil(self.image_dimensions[1] / len(text_lines[i]))
                y = math.ceil(self.image_dimensions[0] / (len(text_lines) - 1))
                draw.text((j * x, i * y), char, font=self.text_font, spacing=0, fill=char_color, align="left")
        return im

    def draw_text_on_image(self, text: str, background_color: tuple, text_color: tuple):
        im = Image.new(mode="RGB", size=(self.image_dimensions[1], self.image_dimensions[0]), color=background_color)
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), text, font=self.text_font, spacing=0, fill=text_color, align ="left")
        return im


if __name__ == "__main__":

    iag = ImageAsciiGenerator(8, " .-;+=xX$", True)
    edited_image = iag.load_image()
    final_text = iag.pixels_to_text(edited_image)
    background_color = (22, 3, 43)
    foreground_color = (0, 195, 255)
    im = iag.draw_text_on_img_adjusted(final_text, background_color, foreground_color)
    im.show()
    ask = False
    if not iag.TEST and ask:
        if input("Do you want to save? (y/n) ") == 'y':
            image_name = input("What do you want to name the image?\n")
            im.save(f'images\{image_name}.png')
