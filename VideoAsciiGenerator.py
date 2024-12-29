import cv2 as cv
from helper import Helper
from moviepy import AudioFileClip, VideoFileClip, ImageSequenceClip, VideoClip
from ImageAsciiGenerator import ImageAsciiGenerator
import numpy as np
import time
import warnings
from Effect import Effect


class VideoAsciiGenerator:

    def __init__(self, video, font_size=8, gradient=' .-;+=xX$█', use_contrast=False, background_color=(66, 5, 5),
                 foreground_color=(164, 255, 45), video_start=None, video_end=None, effect=None):
        self.video = video
        self.font_size = font_size
        self.gradient = gradient
        self.use_contrast = use_contrast
        self.bg_color = background_color
        self.fg_color = foreground_color
        self.video_start = video_start
        self.video_end = video_end
        self.effect = effect

    def convert(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            video_frames, fps = self.__get_video_frames()
        text_frames = self.__frames_to_text(video_frames)
        video = self.__frames_to_video(text_frames, fps)
        audio = self.__extract_audio()
        final = self.__combine_video_audio(video, audio)
        self.__save_video(final)

    def __frames_to_text(self, video_frames):
        text_frames = []
        start_time = time.time()
        if self.effect == Effect.VIDEO_RAINBOW_GRADUAL:
            bg_color = (0, 0, 0)
        else:
            bg_color = self.bg_color

        Helper.print_progress_bar(iteration=0, total=len(video_frames), prefix="Converting images")
        for i, frame in enumerate(video_frames):
            if self.effect == Effect.VIDEO_RAINBOW_GRADUAL:
                hue = (2 * i) % 181  # for some reason, hue has range 0 - 180
                fg_color = Helper.hsv_to_rgb((hue, 1, 1))
                effect = None
            else:
                fg_color = self.fg_color
                effect = self.effect
            og_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            iag = ImageAsciiGenerator(image=og_img, font_size=self.font_size, ascii_gradient=self.gradient,
                                      use_contrast=self.use_contrast, background_color=bg_color,
                                      foreground_color=fg_color, effect=effect)

            Helper.print_progress_bar(iteration=i + 1, total=len(video_frames), prefix="Converting images")
            converted = iag.convert()
            text_frames.append(np.array(converted))
        end_time = time.time()
        print(f'\n-----FRAMES CONVERTED IN {end_time - start_time} SECONDS-----')
        return text_frames

    def __extract_audio(self):
        audio_clip = AudioFileClip(self.video)
        aud_start, aud_end = self.__get_clip_timestamps(audio_clip)
        return audio_clip.subclipped(aud_start, aud_end)

    def __get_clip_timestamps(self, clip):
        if self.video_start is None:
            vid_start = 0
        else:
            print(f'Video starting at {self.video_start}')
            vid_start = self.video_start

        if self.video_end is None:
            vid_end = clip.end
        else:
            print(f'Video ending at {self.video_end}')
            vid_end = self.video_end
        return vid_start, vid_end

    def __get_video_frames(self):
        video = VideoFileClip(self.video)
        vid_start, vid_end = self.__get_clip_timestamps(video)

        video = video.subclipped(vid_start, vid_end)
        fps = video.fps
        duration = video.duration
        num_frames = int(fps * duration)
        print("-------VIDEO INFORMATION-------")
        print(f'Video duration: {duration}')
        print(f'Video start: {vid_start}')
        print(f'Video end: {vid_end}')
        print(f'FPS: {fps}')
        print(f'Total frames: {num_frames}')
        print("--------------------------------")
        frame_timestamp = duration / num_frames
        frames = []
        start_time = time.time()
        for i in range(num_frames):
            Helper.print_loading_bar(iteration=i, prefix="Extracting frames")
            frames.append(video.frame_function(i * frame_timestamp))
        end_time = time.time()
        print(f'\n-----FRAMES EXTRACTED IN {end_time - start_time} SECONDS-----')
        return frames, fps

    def __frames_to_video(self, frames, fps):
        video = ImageSequenceClip(sequence=frames, fps=fps)
        return video

    def __combine_video_audio(self, video: VideoFileClip, audio: AudioFileClip):
        final_clip = video.with_audio(audio)
        return final_clip

    def __save_video(self, final_clip: VideoClip):
        video_name = input("What do you want to name the video?\n")
        final_clip.write_videofile(f'./images/{video_name}.mp4')
        final_clip.close()


if __name__ == "__main__":
    vid = Helper.get_file()
    vg = VideoAsciiGenerator(video=vid, font_size=5, gradient="       .-;+=xX$█", foreground_color=(46, 126, 255),
                             background_color=(2, 0, 23), effect=Effect.RAINBOW_HORIZONTAL)
    vg.convert()
