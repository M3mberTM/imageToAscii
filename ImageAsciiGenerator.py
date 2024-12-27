import numpy as np
import cv2 as cv
from PIL import Image, ImageFont, ImageDraw
import math
from helper import Helper
from io import StringIO

# some gradients to play with

#  $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.
#  .-;+=xX$█
#  █$Xx=+;-.


class ImageAsciiGenerator:
    """
    Class for creating images made out of text using an original image.

    Attributes
    ----------
    text_size: int
        size of the font which is used
    text_font: ImageFont
        actual font object using PIL library
    image: np.array
        original image
    image_dimensions: tuple
        overall shape of the image (Dimensions)
    use_contrast: bool
        Boolean value whether to use the higher contrast function or no
    bg_color: tuple
        Background color of the final text image
    fg_color: tuple
        Represents the text color of the final text image
    ascii_gradient: str
        A text brightness gradient given as a string

    Methods
    -------
    convert()
        Converts the original image into the text image and returns it back as a PIL image
    """

    height_width_ratio = 2

    def __init__(self, image: np.array, font_size=8, ascii_gradient=' .-;+=xX$█', use_contrast=False,
                 background_color=(66, 5, 5), foreground_color=(164, 255, 45), invert_gradient=False):
        """ImageAsciiGenerator

        :param image: original image to be converted
        :param font_size: size of the text to use in the final image
        :param ascii_gradient: brightness gradient of text which the pixels are mapped to
        :param use_contrast: Chooses whether to use higher method for higher contrast
        :param background_color: Color of the background in the final image
        :param foreground_color: Color of the text in the final image
        :param invert_gradient: Whether to reverse the gradient
        """
        self.text_size = font_size
        if invert_gradient:
            self.ascii_gradient = ascii_gradient[::-1]
        else:
            self.ascii_gradient = ascii_gradient
        # monospace fonts: consolaz, cour, lucon
        self.text_font = ImageFont.truetype("lucon.ttf", self.text_size)
        self.width_divisor = self.text_size
        self.height_divisor = self.width_divisor
        self.image = image
        self.image_dimensions = np.shape(self.image)
        self.use_contrast = use_contrast
        self.bg_color = background_color
        self.fg_color = foreground_color
        self.divider = 255 / (len(self.ascii_gradient) - 1)


    def convert(self) -> Image:
        """Main function of the ImageAsciiGenerator Class

        :returns: Image: final image in PIL format
        """
        resized = self.__adjust_image()
        final_txt = self.__pixels_to_txt(resized)
        if self.use_contrast:
            return self.__draw_text_on_img_with_contrast(final_txt)
        else:
            return self.__draw_text_on_image(final_txt)

    def __get_gradient_index(self, brightness: float):
        # limits the range of values to just x values, where x represents the length of the gradient
        return int(brightness // self.divider)

    def __pixels_to_txt(self, resized_img) -> str:
        # uses StringIO to save up on memory
        text_image = StringIO("")
        for i in range(len(resized_img)):
            row = resized_img[i]
            for j in range(len(row)):
                current_char = self.ascii_gradient[self.__get_gradient_index(row[j][2])]
                text_image.write(current_char)
                text_image.write(current_char)
            text_image.write("\n")
        return text_image.getvalue()

    def __adjust_image(self):
        # scales the image down to save up on processing and to take into account the font size
        new_width = math.floor(self.image_dimensions[1] / self.width_divisor)
        new_height = math.floor(self.image_dimensions[0] / self.height_divisor)
        resized_img = cv.resize(self.image, (new_width, new_height))
        return resized_img

    def __draw_text_on_img_with_contrast(self, text: str):
        text_lines = text.split("\n")
        # due to text ending in new character line, need to use len(text_lines) - 1 to avoid the last empty line
        new_height = math.floor((len(text_lines) - 1) * self.text_size)
        new_width = math.floor(len(text_lines[0]) * (self.text_size / self.height_width_ratio))
        im = Image.new(mode="RGB", size=(new_width, new_height),
                       color=self.bg_color)
        draw = ImageDraw.Draw(im)

        # get the difference between foreground and background to only change the color until it becomes background
        # improves the contrast of the image
        back_for_diff = (
            self.fg_color[0] - self.bg_color[0], self.fg_color[1] - self.bg_color[1],
            self.fg_color[2] - self.bg_color[2])
        # the last line is just an empty string due to the \n character being at the end
        for i in range(len(text_lines) - 1):
            for j, char in enumerate(text_lines[i]):
                gradient_length = len(self.ascii_gradient) - 1
                current_char_position = self.ascii_gradient.index(char)
                divisor = math.floor((current_char_position / gradient_length) * 10) / 10

                char_color = (math.floor(self.fg_color[0] - (back_for_diff[0] * (1 - divisor))),
                              math.floor(self.fg_color[1] - (back_for_diff[1] * (1 - divisor))),
                              math.floor(self.fg_color[2] - (back_for_diff[2] * (1 - divisor))))
                x = j * (self.text_size / self.height_width_ratio)
                y = i * self.text_size
                draw.text((x, y), char, font=self.text_font, spacing=0, fill=char_color, align="left")
        return im

    def __draw_text_on_image(self, text: str):
        new_height = self.image_dimensions[0]
        new_width = math.floor(self.image_dimensions[1] * 1.2)
        im = Image.new(mode="RGB", size=(new_width, new_height), color=self.bg_color)
        draw = ImageDraw.Draw(im)
        draw.multiline_text((0, 0), text, font=self.text_font, spacing=1, fill=self.fg_color, align="left")
        return im


if __name__ == "__main__":
    test_file_path = "./testImages/cyberpunkGasMask.png"  # test image size 1664 x 1664
    TEST = False
    if not TEST:
        filename = Helper.get_file()
    else:
        filename = test_file_path
    font_size = 8
    gradient = "       .-;+=xX$█"
    background_color = (2, 0, 23)
    foreground_color = (46, 126, 255)
    original_img = Helper.load_image(filename)
    iag = ImageAsciiGenerator(font_size=font_size, ascii_gradient=gradient, image=original_img, use_contrast=True,
                              background_color=background_color, foreground_color=foreground_color)
    final_img = iag.convert()
    final_img.show()
    ask = False
    if not TEST and ask:
        if input("Do you want to save? (y/n) ") == 'y':
            image_name = input("What do you want to name the image?\n")
            final_img.save(f'images\{image_name}.png')
