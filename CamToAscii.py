import cv2 as cv
import numpy as np
import time
from ImageAsciiGenerator import ImageAsciiGenerator


class CamToAscii:

    def __init__(self, ascii_gradient="   .-;+=xX$█", background_color=(66, 5, 5), foreground_color=(164, 255, 45),
                 font_size=8, invert_gradient=False):
        self.ascii_gradient = ascii_gradient
        self.fg_color = foreground_color
        self.bg_color = background_color
        self.font_size = font_size
        self.invert_gradient = invert_gradient

    def convert(self):
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
                # Display the captured frame

                iag = ImageAsciiGenerator(image=frame, ascii_gradient=self.ascii_gradient,
                                          foreground_color=self.fg_color,
                                          background_color=self.bg_color, font_size=self.font_size, invert_gradient=self.invert_gradient)
                result = iag.convert()
                result = np.array(result)
                result = cv.cvtColor(result, cv.COLOR_BGR2RGB)
                cv.imshow('Result', result)

                curr_time = time.time()

            # Press 'q' to exit the loop
            if cv.waitKey(1) == ord('q'):
                break

        # Release the capture and writer objects
        cap.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    gradient = ' .-;+=xX$█'
    background_color = (2, 0, 23)
    foreground_color = (46, 126, 255)
    cta = CamToAscii(ascii_gradient=gradient, font_size=5, foreground_color=foreground_color, background_color=background_color, invert_gradient=True)
    cta.convert()
