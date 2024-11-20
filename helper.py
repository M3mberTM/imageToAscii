import cv2 as cv
import math
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
class Helper:

    @staticmethod
    def load_image(filename:str) -> list[list]:
        img = cv.imread(filename, cv.IMREAD_COLOR)
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # image_dimensions = np.shape(img)

        # new_width = math.floor(image_dimensions[1] / width_divisor)
        # new_height = math.floor(image_dimensions[0] / height_divisor)
        # resized_img = cv.resize(img, (new_width, new_height))
        return img

    @staticmethod
    def get_file():
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()
        return filename
