import cv2 as cv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys


class Helper:

    @staticmethod
    def load_image(filename: str) -> list[list]:
        img = cv.imread(filename, cv.IMREAD_COLOR)
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        return img

    @staticmethod
    def get_file():
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()
        return filename

    @staticmethod
    def print_progress_bar(iteration: int, total: int, prefix='', suffix='', fill='█'):
        length = 50
        percentage = ("{0:.2f}").format(100 * (iteration / float(total)))
        filled = int(length * (iteration / total))
        bar = f'|{fill * filled}{"-" * (length - filled)}|'
        text = f'{prefix}{bar} {percentage}% {suffix}'

        sys.stdout.write(f'\r{text}')
        sys.stdout.flush()
        # Progress: |█████████████████████████████████████████████-----| 90.0% Complete

    @staticmethod
    def print_loading_bar(iteration, prefix='Loading'):
        steps = '|/-\\'
        current = steps[iteration % len(steps)]
        text = f'{prefix}...  {current}'
        sys.stdout.write(f'\r{text}')
        sys.stdout.flush()
