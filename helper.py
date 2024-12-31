import cv2 as cv
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import sys


class Helper:
    """Helper class containing useful methods which are used throughout the whole project

    Methods
    -------
    load_image(filename: str)
        loads an image based on the filepath as a numpy array converted to HSV mode
    get_file
        opens file dialog and allows user to select a file
    hsv_to_rgb(hsv_color: tuple[3])
        converts given hsv color to its rgb equivalent. HSV is defined with max values of (180, 1, 1)
    print_progress_bar(iteration: int, total: int, prefix='', suffix='', fill='█')
        prints progress bar into console with percentage completion
    print_loading_bar(iteration, prefix='Loading')
        prints loading bar into console. Useful for times when user is uncertain how long a function takes
    """

    @staticmethod
    def load_image(filename: str) -> list[list]:
        """Loads and converts an image into HSV color mode

        :param filename: str: filepath to the file to load
        :return: numpy array representation of the loaded image
        """
        img = cv.imread(filename, cv.IMREAD_COLOR)
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        return img

    @staticmethod
    def get_file():
        """Prompts the user with file dialog and returns the selected file

        :return: file path to the selected file
        """
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()
        if len(filename) < 1:
            print("No file was selected. Exiting...")
            exit(1)
        return filename

    @staticmethod
    def get_directory():
        """Prompts the user with a file dialog and returns the directory picked

        :return: file path to the selected directory
        """
        Tk().withdraw()
        directory = askdirectory()
        if len(directory) < 1:
            print("No directory was selected. Exiting...")
            return None
        return directory

    @staticmethod
    def hsv_to_rgb(hsv_color):
        """Converts given HSV color to its RGB equivalent

        :param hsv_color: tuple[3]: HSV color in tuple or list format with max values (180, 1, 1)
        :return: RGB color in (255, 255, 255) tuple format
        """
        c = hsv_color[1] * hsv_color[2]
        h = hsv_color[0] / 30
        x = c * (1 - abs((h % 2) - 1))
        m = hsv_color[1] - c

        x = int((x + m) * 255)
        c = int((c + m) * 255)
        m = int(m * 255)
        if 0 <= h < 1:
            return c, x, m
        elif 1 <= h < 2:
            return x, c, m
        elif 2 <= h < 3:
            return m, c, x
        elif 3 <= h < 4:
            return m, x, c
        elif 4 <= h < 5:
            return x, m, c
        else:
            return c, m, x

    @staticmethod
    def print_progress_bar(iteration: int, total: int, prefix='', suffix='', fill='█'):
        """Prints a progress bar into the console with a percentage progress

        :param iteration: int: Current progress
        :param total: int: Total amount to be reached
        :param prefix: str: Text to be written in front of the progress bar
        :param suffix: str: Text to be written at the end of the progress bar
        :param fill: str: Character to be used for filling in the progress bar
        """
        length = 50
        percentage = ("{0:.2f}").format(100 * (iteration / float(total)))
        filled = int(length * (iteration / total))
        bar = f'|{fill * filled}{"-" * (length - filled)}|'
        text = f'{prefix}{bar} {percentage}% {suffix}'

        sys.stdout.write(f'\r{text}')
        sys.stdout.flush()
        # Progress: |█████████████████████████████████████████████-----| 90.0% Complete

    @staticmethod
    def print_loading_bar(iteration: int, prefix='Loading'):
        """Prints a loading bar into the console with an animation

        :param iteration: int: Current progress of the task
        :param prefix: str:  Text to be written in front of the loading animation
        """
        steps = '▁▂▃▄▅▆▇▉'
        current = steps[iteration % len(steps)]
        text = f'{prefix}...  {current}'
        sys.stdout.write(f'\r{text}')
        sys.stdout.flush()
