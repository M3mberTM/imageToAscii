import numpy as np
import cv2 as cv
import math
from helper import Helper
from io import StringIO


class CMDAsciiGenerator:
    """
    Class for converting images into text in the console.

    Attributes
    ----------
    width_height_ratio: int
        width to height ratio of characters in terminal window
    image: np.array
        original image to be converted
    terminal_width: int
        maximum width the image should be in order to fit into the terminal window
    ascii_gradient: str
        a text representing brightness gradient which the pixels are mapped to

    Methods
    -------
    convert()
        converts the image into the text based on the arguments given in the constructor
    """

    width_height_ratio = 3
    result = None

    def __init__(self, image: np.array, terminal_width=220, ascii_gradient=" .-;+=xX$█", invert_gradient=False):
        """CMDAsciiGenerator constructor

        :param image: image to be converted
        :param terminal_width: maximum wanted width of the image in terminal
        :param ascii_gradient: brightness gradient given as a string which the pixels are mapped to
        :param invert_gradient: reverses the gradient
        """

        self.image = image
        self.ascii_gradient = ascii_gradient[::-1] if invert_gradient else ascii_gradient
        self.terminal_width = int(terminal_width // self.width_height_ratio)
        self.divider = 255 / (len(self.ascii_gradient) - 1)

    def __get_gradient_index(self, brightness: float) -> int:
        # limits range to x values to match the amount of characters in the gradient and returns one based on brightness
        return int(brightness // self.divider)

    def convert(self) -> str:
        """Main function. Converts given image into text based on the brightness values. Returns String.

        :returns: str: image in text form
        """

        resized = self.__adjust_image()
        self.result = self.__pixels_to_txt(resized)
        return self.result

    def show_result(self):
        """Shows the result of the class. Should be called after convert method"""
        print(f'\n\x1b[94m{self.result}\x1b[0m')

    def __adjust_image(self) -> list[list]:
        # converts into HSV to use Value later for getting the correct character from gradient
        img = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
        img_dimensions = np.shape(img)

        # scales down the image to fit into the terminal and also to lower the amount of comparisons to be done
        scale_ratio = img_dimensions[1] / self.terminal_width
        new_width = math.floor(img_dimensions[1] // scale_ratio)
        new_height = math.floor(img_dimensions[0] // scale_ratio)

        resized_img = cv.resize(img, (new_width, new_height))
        return resized_img

    def __pixels_to_txt(self, resized_img) -> str:
        # uses StringIO to save up on memory
        text_image = StringIO("")

        for i in range(len(resized_img)):
            for j, k in enumerate(resized_img[i]):
                current_char = self.ascii_gradient[self.__get_gradient_index(k[2])]
                # times the character in line by the ratio to combat the different width to height ratio of the text
                text_image.write(current_char * self.width_height_ratio)
            text_image.write("\n")

        return text_image.getvalue()


if __name__ == "__main__":

    test_file_path = "../testImages/cyberpunkGasMask.png"
    TEST = False

    gradient = " .-;+=xX$"
    if not TEST:
        filename = Helper.get_file()
    else:
        filename = test_file_path
    width = int(input("Terminal width:"))
    original_img = Helper.load_image(filename)
    ascii_gen = CMDAsciiGenerator(original_img, width, ascii_gradient=gradient)
    print("\x1b[94m", ascii_gen.convert(), "\x1b[0m")
