from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import cv2 as cv
import math


class CMDAsciiGenerator:
    ascii_gradient = " .-;+=xX$█"
    width_height_ratio = 3
    scale_down_factor = 1.5
    terminal_width: int = int(225 // (width_height_ratio * scale_down_factor))
    test_file_path = "C:\\Users\\risko\\Documents\\Pictures\\Midjourney Beginning of time.png"
    TEST = False
    filename = ""

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
        img_dimensions = np.shape(img)

        scale_ratio = math.ceil(img_dimensions[0] / self.terminal_width)
        new_width = img_dimensions[1] // scale_ratio
        new_height = img_dimensions[0] // scale_ratio

        resized_img = cv.resize(img, (new_width, new_height))
        return resized_img

    def convert(self, resized_img) -> str:
        ascii_img = "\x1b[94m"

        for i in range(len(resized_img)):
            for j, k in enumerate(resized_img[i]):
                current_char = self.ascii_gradient[self.get_index_value(k[2])]
                ascii_img = ascii_img + current_char*self.width_height_ratio
            ascii_img = ascii_img + "\n"
        return ascii_img


if __name__ == "__main__":
    ascii_gen = CMDAsciiGenerator()
    edited_image = ascii_gen.open_image()
    final_image = ascii_gen.convert(edited_image)
    print(final_image)
