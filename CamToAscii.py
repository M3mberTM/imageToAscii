import cv2 as cv
import numpy as np
import time
from ImageAsciiGenerator import ImageAsciiGenerator


class CamToAscii:

    def __init__(self, ascii_gradient="   .-;+=xX$█"):
        self.ascii_gradient = ascii_gradient

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

                frame_dimensions = np.shape(frame)
                scale_factor = 2
                frame = cv.resize(frame, (frame_dimensions[1] * scale_factor, frame_dimensions[0] * scale_factor))
                iag = ImageAsciiGenerator(image=frame, ascii_gradient=self.ascii_gradient,
                                          foreground_color=(46, 126, 255),
                                          background_color=(2, 0, 23), font_size=8, use_contrast=True)
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
    cta = CamToAscii(ascii_gradient=gradient)
    cta.convert()
