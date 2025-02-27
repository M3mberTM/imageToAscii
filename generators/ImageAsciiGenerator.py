import numpy as np
import cv2 as cv
from PIL import Image, ImageFont, ImageDraw
import math
from helper import Helper
from io import StringIO
from Effect import Effect


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
    result = None
    effect_lookup = None

    def __init__(self, image: np.array, font_size=8, ascii_gradient=' .-;+=xX$█', use_contrast=False,
                 background_color=(66, 5, 5), foreground_color=(164, 255, 45), invert_gradient=False, effect=None):
        """ImageAsciiGenerator constructor.

        :param image: original image to be converted
        :param font_size: size of the text to use in the final image
        :param ascii_gradient: brightness gradient of text which the pixels are mapped to
        :param use_contrast: Chooses whether to use higher method for higher contrast
        :param background_color: Color of the background in the final image
        :param foreground_color: Color of the text in the final image
        :param invert_gradient: Whether to reverse the gradient
        :param effect: specific effect to put on the image (can overwrite the color parameters)
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
        self.effect = effect
        self.divider = 255 / (len(self.ascii_gradient) - 1)

    def convert(self) -> Image:
        """Main function of the ImageAsciiGenerator Class

        :returns: Image: final image in PIL format
        """
        resized = self.__adjust_image()
        final_txt = self.__pixels_to_txt(resized)
        self.get_color_array(resized)
        if self.effect is not None:
            self.result = self.__draw_text_on_img_effect(final_txt)
            return self.result

        if self.use_contrast:
            self.result = self.__draw_text_on_img_with_contrast(final_txt)
            return self.result
        else:
            self.result = self.__draw_text_on_img(final_txt)
            return self.result

    def get_color_array(self, adjusted_img: np.array):
        img_shape = np.shape(adjusted_img)
        if self.effect == Effect.RAINBOW_HORIZONTAL:
            self.effect_lookup = self.generate_horizontal_rainbow_array(img_shape, False)
        elif self.effect == Effect.RAINBOW_HORIZONTAL_REV:
            self.effect_lookup = self.generate_horizontal_rainbow_array(img_shape, True)
        elif self.effect == Effect.RAINBOW_VERTICAL:
            self.effect_lookup = self.generate_vertical_rainbow_array(img_shape, False)
        elif self.effect == Effect.RAINBOW_VERTICAL_REV:
            self.effect_lookup = self.generate_vertical_rainbow_array(img_shape, True)
        elif self.effect == Effect.RAINBOW_RADIAL:
            self.effect_lookup = self.generate_radial_rainbow_array(img_shape, False)
        elif self.effect == Effect.RAINBOW_RADIAL_REV:
            self.effect_lookup = self.generate_radial_rainbow_array(img_shape, True)
        elif self.effect == Effect.ORIGINAL_COLOR:
            self.effect_lookup = self.generate_original_color_array(img_shape, adjusted_img, False)
        else:
            self.effect = None
    def generate_original_color_array(self, array_shape: tuple, adjusted_img: np.array, reverse: bool):
        width = array_shape[1]
        height = array_shape[0]
        effect_array = np.zeros(array_shape, dtype=int)
        for row in range(height):
            for col in range(width):
                if not reverse:
                    pixel_color = adjusted_img[row, col]
                    effect_array[row, col] = [int(pixel_color[0]), int(pixel_color[1]), int(pixel_color[2])]
                else:
                    pixel_color = adjusted_img[row, col]
                    effect_array[row, col] = [255 - int(pixel_color[0]), 255 - int(pixel_color[1]), 255 - int(pixel_color[2])]
        return effect_array


    def generate_radial_rainbow_array(self, array_shape: tuple, reverse: bool):
        width = array_shape[1]
        height = array_shape[0]
        effect_array = np.zeros((height, width))
        for row in range(height):
            for col in range(width):
                center = (height // 2, width // 2)
                max_distance = math.ceil(math.sqrt((center[0] ** 2) + (center[1] ** 2)))

                distance = abs(center[0] - row) ** 2 + abs(center[1] - col) ** 2
                distance = math.sqrt(distance)
                center_closeness = (max_distance - distance) / max_distance
                if not reverse:
                    effect_array[row, col] = min(math.floor(center_closeness * 180), 180)
                else:
                    effect_array[row, col] = 180 - min(math.floor(center_closeness * 180), 180)
        return effect_array

    def generate_horizontal_rainbow_array(self, array_shape: tuple, reverse: bool):
        width = array_shape[1]
        height = array_shape[0]
        effect_array = np.zeros((height, width))
        for row in range(height):
            for col in range(width):
                if not reverse:
                    effect_array[row, col] = math.floor((180 / width) * col)
                else:
                    effect_array[row, col] = 180 - math.floor((180 / width) * col)
        return effect_array

    def generate_vertical_rainbow_array(self, array_shape: tuple, reverse: bool):
        width = array_shape[1]
        height = array_shape[0]
        effect_array = np.zeros((height, width))
        for row in range(height):
            for col in range(width):
                if not reverse:
                    effect_array[row, col] = math.floor((180 / height) * row)
                else:
                    effect_array[row, col] = 180 - math.floor((180 / height) * row)
        return effect_array

    def show_result(self):
        self.result.show()
        if input("Do you want to save? (y/n) ") == 'y':
            directory = Helper.get_directory()
            if directory is not None:
                img_name = input("What do you want to name the image? ")
                self.result.save(f'{directory}/{img_name}.png')

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

    def __draw_text_on_img(self, text: str):
        text_lines = text.split("\n")
        row_length = len(text_lines[0])
        new_height = self.image_dimensions[0]
        if self.text_size > 5:
            width_to_height_ratio = 0.6125
        else:
            width_to_height_ratio = 0.6
        # new_width = math.floor(self.image_dimensions[1] * width_to_height_ratio)
        new_width = math.floor(row_length * self.text_size * width_to_height_ratio)
        im = Image.new(mode="RGB", size=(new_width, new_height), color=self.bg_color)
        draw = ImageDraw.Draw(im)
        draw.multiline_text((0, 0), text, font=self.text_font, spacing=1, fill=self.fg_color, align="left")
        return im

    def __draw_text_on_img_effect(self, text):
        text_lines = text.split("\n")
        # due to text ending in new character line, need to use len(text_lines) - 1 to avoid the last empty line
        new_height = math.floor((len(text_lines) - 1) * self.text_size)
        new_width = math.floor(len(text_lines[0]) * (self.text_size / self.height_width_ratio))
        im = Image.new(mode="RGB", size=(new_width, new_height),
                       color=(0, 0, 0))
        draw = ImageDraw.Draw(im)
        total_cols = len(text_lines[0])
        total_rows = len(text_lines)
        # the last line is just an empty string due to the \n character being at the end
        for i in range(len(text_lines) - 1):
            for j, char in enumerate(text_lines[i]):
                # hue = self.__get_effect_hue(row=i, col=j, total_rows=total_rows, total_cols=total_cols)
                hue = self.effect_lookup[i, j//2]
                if self.effect != Effect.ORIGINAL_COLOR:
                    char_color = Helper.hsv_to_rgb((hue, 1, 1))
                else:
                    char_color = Helper.hsv_to_rgb((hue[0], hue[1] / 255, hue[2] / 255))
                x = j * (self.text_size / self.height_width_ratio)
                y = i * self.text_size
                draw.text((x, y), char, font=self.text_font, spacing=0, fill=char_color, align="left")
        return im

    def __get_effect_hue(self, row: int, col: int, total_rows: int, total_cols: int) -> int:
        if self.effect == Effect.RAINBOW_HORIZONTAL:
            return math.floor((180 / total_cols) * col)
        elif self.effect == Effect.RAINBOW_HORIZONTAL_REV:
            return 180 - math.floor((180 / total_cols) * col)
        elif self.effect == Effect.RAINBOW_VERTICAL:
            return math.floor((180 / total_rows) * row)
        elif self.effect == Effect.RAINBOW_VERTICAL_REV:
            return 180 - (180 / total_rows) * row
        elif self.effect == Effect.RAINBOW_RADIAL or self.effect == Effect.RAINBOW_RADIAL_REV:
            center = (total_rows // 2, total_cols // 2)
            max_distance = math.ceil(math.sqrt((center[0] ** 2) + (center[1] ** 2)))

            distance = abs(center[0] - row) ** 2 + abs(center[1] - col) ** 2
            distance = math.sqrt(distance)
            center_closeness = (max_distance - distance) / max_distance
            if self.effect == Effect.RAINBOW_RADIAL:
                return min(math.floor(center_closeness * 180), 180)
            else:
                return 180 - min(math.floor(center_closeness * 180), 180)


if __name__ == "__main__":
    test_file_path = "../testImages/cyberpunkGasMask.png"  # test image size 1664 x 1664
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
    iag = ImageAsciiGenerator(font_size=font_size, ascii_gradient=gradient, image=original_img, use_contrast=False,
                              background_color=background_color, foreground_color=foreground_color,
                              )
    final_img = iag.convert()
    final_img.show()
    ask = False
    if not TEST and ask:
        if input("Do you want to save? (y/n) ") == 'y':
            image_name = input("What do you want to name the image?\n")
            final_img.save(f'images\{image_name}.png')
