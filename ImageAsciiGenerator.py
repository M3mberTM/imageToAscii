from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import cv2 as cv
from PIL import Image, ImageFont, ImageDraw, ImageFilter

#  $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.
#  .-;+=xX$█
#  █$Xx=+;-.
class ImageAsciiGenerator:
    ascii_gradient = " .-;+=xX$"
    test_file_path = "C:\\Users\\risko\\Documents\\Pictures\\IMG_20200704_141627.jpg"
    TEST = False
    filename = ""
    image_dimensions = None
    text_size = 16
    width_divisor = 20
    height_divisor = 14
    text_font = ImageFont.truetype("cour.ttf", text_size)

    def get_index_value(self, brightness: float):
        divider = 255 / (len(self.ascii_gradient)-1)
        return int(brightness // divider)

    def __init__(self):
        if not self.TEST:
            Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
            self.filename = askopenfilename()
        else:
            self.filename = self.test_file_path

    def open_image(self) -> list[list]:
        img = cv.imread(self.filename, cv.IMREAD_COLOR)
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        self.image_dimensions = np.shape(img)

        new_width = self.image_dimensions[1] // self.width_divisor
        new_height = self.image_dimensions[0] // self.height_divisor

        resized_img = cv.resize(img, (new_width, new_height))
        return resized_img

    def convert(self, resized_img) -> str:
        ascii_img = ""

        for i in range(len(resized_img)):
            for j, k in enumerate(resized_img[i]):
                current_char = self.ascii_gradient[self.get_index_value(k[2])]
                ascii_img = ascii_img + current_char + current_char
            ascii_img = ascii_img + "\n"
        return ascii_img

    def draw_on_image(self, text: str, background_color: tuple, text_color: tuple):
        im = Image.new(mode="RGB", size=(self.image_dimensions[1], self.image_dimensions[0]), color=background_color)
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), text, font=self.text_font, spacing=0, fill=text_color, align ="left")
        return im

    def bloom(self, image, text: str, text_color: tuple):
        bloomed_image = image
        bloomed_image.filter(ImageFilter.BoxBlur(4))
        draw = ImageDraw.Draw(bloomed_image)
        draw.text((0, 0), text, font=self.text_font, spacing=0, fill=text_color, align ="left")
        return bloomed_image

if __name__ == "__main__":

    iag = ImageAsciiGenerator()
    edited_image = iag.open_image()
    final_text = iag.convert(edited_image)
    background_color = (22, 3, 43)
    text_color = (0, 195, 255)
    im = iag.draw_on_image(final_text, background_color, text_color)
    im.show()
    if input("Do you want to save? (y/n) ") == 'y':
        image_name = input("What do you want to name the image?\n")
        im.save(f'images\{image_name}.png')
    # bloom_img = iag.bloom(im, final_text, text_color)
    # bloom_img.show()
