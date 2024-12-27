import cv2 as cv
from helper import Helper
from moviepy import AudioFileClip, VideoFileClip, ImageSequenceClip
from ImageAsciiGenerator import ImageAsciiGenerator
import numpy as np


class VideoAsciiGenerator:

    def __init__(self, video, font_size=8, gradient=' .-;+=xX$█', adjusted=False, background_color=(66, 5, 5),
                 foreground_color=(164, 255, 45)):
        self.video = video
        self.font_size = font_size
        self.gradient = gradient
        self.adjusted = adjusted
        self.bg_color = background_color
        self.fg_color = foreground_color

    def convert(self):
        video_frames = self.__get_video_frames()
        text_frames = self.__frames_to_text(video_frames)
        video = self.__frames_to_video(text_frames)
        audio = self.__extract_audio()
        self.__combine_video_audio(video, audio)

    def __frames_to_text(self, video_frames):
        text_frames = []

        Helper.print_progress_bar(iteration=0, total=len(video_frames), prefix="Converting images")
        for i, frame in enumerate(video_frames):
            og_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            iag = ImageAsciiGenerator(image=og_img, font_size=self.font_size, ascii_gradient=self.gradient,
                                      use_contrast=self.adjusted, background_color=self.bg_color,
                                      foreground_color=self.fg_color)

            Helper.print_progress_bar(iteration=i + 1, total=len(video_frames), prefix="Converting images")
            converted = iag.convert()
            text_frames.append(np.array(converted))
        print("\n-----FRAMES CONVERTED-----")
        return text_frames

    def __extract_audio(self):
        audio_clip = AudioFileClip(self.video)
        return audio_clip

    def __get_video_frames(self):
        capture = cv.VideoCapture(self.video)  # load the video
        frame_nr = 0
        frames = []
        while (True):
            success, frame = capture.read()  # read the current frame
            if success:
                frames.append(frame)
            else:
                break
            Helper.print_loading_bar(iteration=frame_nr, prefix="Extracting frames")
            frame_nr = frame_nr + 1
        # added new line character to write on new line instead of the same as the loading bar when extracting
        print("\n-----FRAMES EXTRACTED-----")
        capture.release()
        return frames

    def __frames_to_video(self, frames):
        video = ImageSequenceClip(sequence=frames, fps=30)
        return video

    def __combine_video_audio(self, video: VideoFileClip, audio: AudioFileClip):
        final_clip = video.with_audio(audio)
        final_clip.preview(fps=30)
        video_name = input("What do you want to name the video?\n")
        final_clip.write_videofile(f'./images/{video_name}.mp4')
        final_clip.close()

if __name__ == "__main__":
    vid = Helper.get_file()
    vg = VideoAsciiGenerator(video=vid, font_size=5, gradient="       .-;+=xX$█", foreground_color=(46, 126, 255), background_color=(2, 0, 23))
    vg.convert()
