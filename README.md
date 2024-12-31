# ASCII converter

A simple python app for conversion of images into text (ASCII). Made over several weeks and started as a simple app for
turning an image into text, that will be printed in the console. Eventually turned into wanting to play with the output
more and more, leading me to create an image version, which allows playing with the colors and later a video version and
real time camera version as well. At last, the option to add some simple rainbow effects was added.

## Idea

Several years ago, I stumbled into a video on YouTube by ***The Coding Train*** where he first showcased a technique to
convert images into text.

The technique relies on the fact that different characters are comprised of different amount of pixels, therefore some
characters will look brighter, and some darker. You could call it a sort of screentone.

The technique seemed pretty simple and therefore I created my first app for this conversion in Java a couple of years
ago. However, that old code was pretty terrible. It didn't work well on bigger images and was kind of slow. This didn't
bother me at the time as I was still learning Java and it worked well as a bigger but manageable project for me.

Then, later this year, I came across another video that talked about an improved method. This time, talking about how to
make the edges as well and how to use this as a shader inside of unity. This video pique my interest again in the
project and I sought out to redo this project and do it justice on my part. Now, I don't know how to work with shaders
so I just figured I would do it in python instead.

I started with the simple idea of just turning it into text that I can then copy, however I started to add more and more
features on it until it has turned to this.

The Coding Train video -> [Here](https://youtu.be/55iwMYv8tGI?si=YnE7BKlJ0MBf2yrQ)

The other video -> [Here](https://youtu.be/gg40RWiaHRY?si=SiuouQA0Ry-5Up4F)

## MODES

| Mode  | Description                                                 | CMD Usage    |
|-------|-------------------------------------------------------------|--------------|
| CMD   | Prints the text to console                                  | "cmd" or 0   |
| Image | Creates an image, with adjustable background and text color | "image" or 1 |
| Video | Converts video using the same principles as before          | "video" or 2 |
| Cam   | Converts your live camera feed into image feed              | "cam" or 3   |

## USAGE

There are two ways to run the whole app. First is by opening up an IDE of your choice and going to the preferred
generator. Then, you can just adjust the values down in the '__name__ == "__main__"' up to your liking.

The second way of running the app would be to run the main.py using a terminal and give it the required arguments. There
is only one argument required, which is the `mode` the app should use, given either as text or as int. Currently, there
are 4 modes, which are listed higher. Running the app would be simple as:

```python main.py [mode]```