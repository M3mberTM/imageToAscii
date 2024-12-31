import cv2 as cv
import numpy as np
import time
from generators.ImageAsciiGenerator import ImageAsciiGenerator


class CamToAscii:
    """Class for conversion of webcam images in real time to ascii images.

    Attributes
    ----------
    gradient: str
        text representing brightness gradient that pixels are mapped to. Used in the conversion
    fg_color: tuple[3]
        represents the RGB color to be used for text in the conversion
    bg_color: tuple[3]
        represents the RGB color to be used for background in the conversion
    font_size: int
        size of the text to be used in the conversion

    Methods
    -------
    convert()
        Converts the webcam feed into text
    """
    def __init__(self, gradient="   .-;+=xX$█", background_color=(66, 5, 5), foreground_color=(164, 255, 45),
                 font_size=8, invert_gradient=False, show_webcam=False):
        """Constructor of the CamToAscii class

        :param gradient: text representing the brightness gradient that pixels are mapped to
        :param background_color: represents the RGB color to be used for background in the conversion
        :param foreground_color: represents the RGB color to be used for text in the conversion
        :param font_size: size of the text to be used in the conversion
        :param invert_gradient: reverses the gradient text
        :param show_webcam: chooses whether to show the original webcam as well
        """
        self.gradient = gradient[::-1] if invert_gradient else gradient
        self.fg_color = foreground_color
        self.bg_color = background_color
        self.font_size = font_size
        self.show_webcam = show_webcam

    def convert(self):
        """Main method of the class

        Converts the webcam feed into text images, which are then shown. Press Q to stop the stream.
        """
        # Open the default camera
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            Exception("Cannot open camera")
        curr_time = time.time()
        while True:
            ret, frame = cap.read()
            diff = time.time() - curr_time

            if not ret:
                Exception("Couldn't load the camera stream")

            if diff > 0.3:
                iag = ImageAsciiGenerator(image=frame, ascii_gradient=self.gradient,
                                          foreground_color=self.fg_color,
                                          background_color=self.bg_color, font_size=self.font_size)
                result = iag.convert()
                result = np.array(result)
                result = cv.cvtColor(result, cv.COLOR_BGR2RGB)
                cv.imshow('Result', result)

                curr_time = time.time()
            if self.show_webcam:
                cv.imshow('Webcam', frame)
            # Press 'q' to exit the loop
            if cv.waitKey(1) == ord('q'):
                print("Exiting...")
                break

        cap.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    gradient = ' .-;+=xX$█'
    background_color = (2, 0, 23)
    foreground_color = (46, 126, 255)
    cta = CamToAscii(gradient=gradient, font_size=5, foreground_color=foreground_color, background_color=background_color, invert_gradient=True)
    cta.convert()
