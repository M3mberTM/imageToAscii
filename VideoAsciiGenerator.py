import cv2 as cv
from PIL import Image
import os
from ImageAsciiGenerator import ImageAsciiGenerator
import numpy as np
class VideoAsciiGenerator:

    def video_to_frames(self):
        capture = cv.VideoCapture('./testImages/S3rl_Play_it_loud.mp4')  # load the video
        frame_nr = 0

        while (True):
            success, frame = capture.read()  # read the current frame
            if success:
                cv.imwrite(f'./videoFrames/{frame_nr}.jpg', frame)

            else:
                break
            frame_nr = frame_nr+1

        capture.release()

    def cv_img_to_pil(self, image):
        color_coverted = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        pil_image = Image.fromarray(color_coverted)
        return pil_image


    def generate_video(self, frames):

        video_name = 'mygeneratedvideo.avi'

        images = frames
        image_folder = "./images"
        # Set frame from the first image
        frame = frames[0]
        height, width, layers = frame.shape

        # Video writer to create .avi file
        video = cv.VideoWriter(f'{image_folder}/{video_name}', cv.VideoWriter_fourcc(*'DIVX'), 20, (width, height))

        # Appending images to video
        for image in images:
            video.write(image)

        # Release the video file
        video.release()
        cv.destroyAllWindows()
        print("Video generated successfully!")


if __name__ == "__main__":
    vg = VideoAsciiGenerator()
    # vg.video_to_frames()
    image_folder = "./videoFrames"
    frames = []
    images = [img for img in os.listdir(image_folder) if img.endswith((".jpg", ".jpeg", ".png"))]
    for i in range(len(images)):
        print(f'{i}/{len(images)}')
        iag = ImageAsciiGenerator(8, " .-;+=xX$", os.path.join(image_folder, images[i]))
        edited_img = iag.adjust_image()
        final_text = iag.pixels_to_text(edited_img)
        background_color = (51, 12, 0)
        foreground_color = (64, 255, 0)
        im = iag.draw_text_on_img_adjusted(final_text, background_color, foreground_color)
        im_convert = im.convert('RGB')
        open_cv_image = np.array(im_convert)
        frames.append(open_cv_image)

    vg.generate_video(frames)